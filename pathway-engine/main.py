# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

import ingestions
from ingestions import IngestItem, IngestResponse
from workload import compute_workload_index, detect_stress
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
    return {
        "assignments": len(ingestions.assignments),
        "exams": len(ingestions.exams),
        "events": len(ingestions.events),
    }


@app.post("/query/ask")
def ask_question(req: AskRequest):
    context = build_context()
    answer = ask_llm(context, req.question)

    return {
        "question": req.question,
        "answer": answer,
        "facts": {
            "assignments": len(ingestions.assignments),
            "exams": len(ingestions.exams),
            "events": len(ingestions.events),
        },
        "timestamp": datetime.utcnow().isoformat()
    }
