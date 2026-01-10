from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

import ingestions
from workload import compute_workload
from llm import ask_llm, build_context
from storage import load_data, save_data

app = FastAPI(title="Improved Stress Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
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

# --- Routes ---

@app.post("/ingest")
def ingest(data: ingestions.IngestItem):
    ingestions.ingest_item(data)
    return {"status": "ok"}

@app.post("/query/ask")
def ask_question(req: AskRequest):
    # Fix: build_context() now refreshes data and includes titles/days
    context = build_context() 
    
    # Calculate current stress stats for the UI cards
    workload = compute_workload(ingestions.assignments, ingestions.exams, ingestions.events)
    
    answer = ask_llm(context, req.question)

    return {
        "answer": answer,
        "facts": {
            "assignments": len(ingestions.assignments),
            "exams": len(ingestions.exams),
            "events": len(ingestions.events),
            "stress_level": workload["stress_level"],
            "workload_score": workload["score"]
        }
    }

@app.get("/data/all")
def get_all():
    return load_data()

@app.delete("/data/delete")
def delete_item(item: DeleteItem): # It must take the model as an argument
    data = load_data()
    if item.category not in data or item.index >= len(data[item.category]):
        return {"error": "Invalid index or category"}

    target = data[item.category][item.index]
    if item.title is not None: target["title"] = item.title
    if item.due_in_days is not None: target["due_in_days"] = item.due_in_days

    save_data(data["assignments"], data["exams"], data["events"])
    ingestions.refresh_from_disk() # Critical for syncing memory
    return {"status": "updated"}


@app.delete("/data/delete")
def delete_item(category: str, index: int): # Parameters moved from model to URL
    data = load_data()

    if category not in data:
        return {"error": "Invalid category"}

    if index < 0 or index >= len(data[category]):
        return {"error": "Index out of range"}

    # Remove the item using the verified category and index
    removed = data[category].pop(index)

    # Save the updated data state to disk
    save_data(
        data["assignments"],
        data["exams"],
        data["events"]
    )

    ingestions.refresh_from_disk() # Sync in-memory data
    return {"status": "deleted", "removed": removed}

@app.get("/health")
def health_check():
    return {"status": "ok"}



