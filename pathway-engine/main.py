from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

import ingestions
from ingestions import refresh_from_disk, IngestItem, IngestResponse
from workload import compute_workload
from llm import ask_llm
from storage import load_data, save_data

app = FastAPI(title="Stress Load Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# MODELS
# -----------------------------

class AskRequest(BaseModel):
    question: str

class UpdateItem(BaseModel):
    category: str
    index: int
    title: Optional[str] = None
    due_in_days: Optional[int] = None

class DeleteItem(BaseModel):
    category: str
    index: int

# -----------------------------
# INGEST
# -----------------------------

@app.post("/ingest", response_model=IngestResponse)
def ingest(data: IngestItem):
    ingestions.ingest_item(data)
    return {"status": "ok", "message": "Data ingested"}

# -----------------------------
# QUERY + AI
# -----------------------------

@app.post("/query/ask")
def ask_question(req: AskRequest):
    refresh_from_disk()

    workload = compute_workload(
        ingestions.assignments,
        ingestions.exams,
        ingestions.events
    )

    context = f"""
Stress Level: {workload['stress_level']}
Workload Score: {workload['score']}
Assignments: {len(ingestions.assignments)}
Exams: {len(ingestions.exams)}
Events: {len(ingestions.events)}
"""

    answer = ask_llm(context, req.question)

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

# -----------------------------
# DATA VIEW
# -----------------------------

@app.get("/data/all")
def get_all_data():
    return load_data()

# -----------------------------
# UPDATE ITEM (FIXED)
# -----------------------------

@app.put("/data/update")
def update_item(item: UpdateItem):
    data = load_data()

    if item.category not in data:
        return {"error": "Invalid category"}

    if item.index < 0 or item.index >= len(data[item.category]):
        return {"error": "Index out of range"}

    raw = data[item.category][item.index]

    # Normalize bad data
    if isinstance(raw, str):
        target = {
            "type": item.category[:-1],
            "title": raw,
            "due_in_days": 0
        }
    elif isinstance(raw, dict):
        target = raw
    else:
        return {"error": "Corrupted data"}

    if item.title is not None:
        target["title"] = item.title

    if item.due_in_days is not None:
        target["due_in_days"] = item.due_in_days

    data[item.category][item.index] = target

    save_data(
        data["assignments"],
        data["exams"],
        data["events"]
    )
    refresh_from_disk()

    return {"status": "updated", "item": target}

# -----------------------------
# DELETE ITEM (FIXED)
# -----------------------------

@app.delete("/data/delete")
def delete_item(item: DeleteItem):
    data = load_data()

    if item.category not in data:
        return {"error": "Invalid category"}

    if item.index < 0 or item.index >= len(data[item.category]):
        return {"error": "Index out of range"}

    removed = data[item.category].pop(item.index)

    save_data(
        data["assignments"],
        data["exams"],
        data["events"]
    )

    refresh_from_disk()
    return {"status": "deleted", "removed": removed}
