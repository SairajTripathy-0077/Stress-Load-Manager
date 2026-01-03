from fastapi import FastAPI
from datetime import datetime

import ingestions   # ✅ IMPORTANT
from ingestions import IngestItem, IngestResponse
from workload import compute_workload_index, detect_stress
from vectors import explain_workload

app = FastAPI(title="Stress Load Manager")


@app.post("/ingest", response_model=IngestResponse)
def ingest(data: IngestItem):
    ingestions.ingest_item(data)
    return {
        "status": "ok",
        "message": "Data ingested successfully"
    }


@app.get("/debug/state")
def debug_state():
    return {
        "assignments": len(ingestions.assignments),
        "exams": len(ingestions.exams),
        "events": len(ingestions.events),
    }


@app.get("/query/summary")
def workload_summary():
    load = compute_workload_index()
    stress = detect_stress(load)

    streams = {
        "assignments": len(ingestions.assignments),
        "exams": len(ingestions.exams),
        "events": len(ingestions.events),
    }

    explanation = explain_workload(load, stress, streams)

    return {
        "workloadIndex": load,
        "stressLevel": stress,
        "streams": streams,
        "explanation": explanation,
        "updatedAt": datetime.utcnow().isoformat()
    }
