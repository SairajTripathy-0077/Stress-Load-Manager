from fastapi import FastAPI
from datetime import datetime
from typing import List

from pydantic import BaseModel
from typing import Dict

class WorkloadSummary(BaseModel):
    workloadIndex: int
    stressLevel: str
    streams: Dict[str, int]
    updatedAt: str


app = FastAPI(title="Pathway-Style Stress Load Engine")

# -----------------------------
# STREAMING TABLES (IN-MEMORY)
# -----------------------------

assignments: List[dict] = []
exams: List[dict] = []
events: List[dict] = []

# -----------------------------
# INGESTION ENDPOINTS (STREAMS)
# -----------------------------

@app.post("/ingest/assignment")
def ingest_assignment(data: dict):
    data["ingested_at"] = datetime.utcnow().isoformat()
    assignments.append(data)
    return {"status": "assignment streamed"}

@app.post("/ingest/exam")
def ingest_exam(data: dict):
    data["ingested_at"] = datetime.utcnow().isoformat()
    exams.append(data)
    return {"status": "exam streamed"}

@app.post("/ingest/event")
def ingest_event(data: dict):
    data["ingested_at"] = datetime.utcnow().isoformat()
    events.append(data)
    return {"status": "event streamed"}

# -----------------------------
# INCREMENTAL COMPUTATION
# -----------------------------

def compute_workload_index():
    load = 0

    for a in assignments:
        load += int(a.get("weight", 1))

    for e in exams:
        load += int(e.get("importance", 2))

    for ev in events:
        load += int(ev.get("duration_hours", 1))

    return load

def detect_stress(load: int):
    if load >= 15:
        return "Extreme Stress"
    elif load >= 10:
        return "High Stress"
    elif load >= 5:
        return "Moderate"
    return "Low"

# -----------------------------
# ANALYTICAL QUERY (PATHWAY-LIKE)
# -----------------------------
@app.get("/query/summary", response_model=WorkloadSummary)
def workload_summary():
    load = compute_workload_index()
    stress = detect_stress(load)

    return {
        "workloadIndex": load,
        "stressLevel": stress,
        "streams": {
            "assignments": len(assignments),
            "exams": len(exams),
            "events": len(events),
        },
        "updatedAt": datetime.utcnow().isoformat()
    }

# -----------------------------
# SIMPLE SEMANTIC Q&A
# -----------------------------

@app.post("/query/ask")
def ask_question(data: dict):
    question = data.get("question", "").lower()
    load = compute_workload_index()
    stress = detect_stress(load)

    if "overload" in question or "stress" in question:
        return {
            "answer": f"Your current workload index is {load}, indicating {stress}."
        }

    if "skip" in question or "attendance" in question:
        if stress in ["High Stress", "Extreme Stress"]:
            return {
                "answer": "Yes, workload peaks may negatively affect attendance."
            }
        return {
            "answer": "Attendance impact is unlikely with the current workload."
        }

    return {
        "answer": "This question will be handled by vector search in Pathway deployment."
    }
