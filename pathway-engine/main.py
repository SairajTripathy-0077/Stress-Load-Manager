# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

import ingestions
from ingestions import refresh_from_disk
from ingestions import IngestItem, IngestResponse
from workload import compute_workload
from llm import ask_llm, build_context

app = FastAPI(title="Stress Load Manager")


# ✅ REQUIRED MODEL (THIS FIXES AskRequest ERROR)
class AskRequest(BaseModel):
    question: str


@app.post("/ingest", response_model=IngestResponse)
def ingest(data: IngestItem):
    ingestions.ingest_item(data)
    return {"status": "ok", "message": "Data ingested"}


@app.get("/debug/state")
def debug_state():
    refresh_from_disk()
    return {
        "assignments": len(ingestions.assignments),
        "exams": len(ingestions.exams),
        "events": len(ingestions.events),
    }


@app.post("/query/ask")
def ask_question(req: AskRequest):
    refresh_from_disk()
    # 1️⃣ Compute workload intelligence
    workload = compute_workload(
        ingestions.assignments,
        ingestions.exams,
        ingestions.events
    )

    # 2️⃣ Build AI-safe context (NO hallucinations)
    context = f"""
WORKLOAD SUMMARY:
Stress level: {workload['stress_level']}
Workload score: {workload['score']}

DUE TODAY:
Assignments: {len(workload['today']['assignments'])}
Exams: {len(workload['today']['exams'])}
Events: {len(workload['today']['events'])}

DUE THIS WEEK:
Assignments: {len(workload['this_week']['assignments'])}
Exams: {len(workload['this_week']['exams'])}
Events: {len(workload['this_week']['events'])}

DUE LATER:
Assignments: {len(workload['later']['assignments'])}
Exams: {len(workload['later']['exams'])}
Events: {len(workload['later']['events'])}
"""

    # 3️⃣ Ask LLM with structured reasoning
    answer = ask_llm(context, req.question)

    # 4️⃣ Return clean response
    return {
        "question": req.question,
        "answer": answer,
        "facts": {
            "assignments": len(ingestions.assignments),
            "exams": len(ingestions.exams),
            "events": len(ingestions.events),
            "stress_level": workload["stress_level"],
            "workload_score": workload["score"]
        },
        "timestamp": datetime.utcnow().isoformat()
    }




