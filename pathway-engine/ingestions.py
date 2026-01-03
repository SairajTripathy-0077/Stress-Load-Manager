# ingestions.py
from pydantic import BaseModel
from typing import Literal
from storage import load_data, save_data

# Load persisted data at startup
_data = load_data()

# In-memory stores (synced with disk)
assignments = _data["assignments"]
exams = _data["exams"]
events = _data["events"]

class IngestItem(BaseModel):
    type: Literal["assignment", "exam", "event"]
    title: str
    due_in_days: int

def ingest_item(item: IngestItem):
    # Convert to plain dict (same as before)
    doc = {
        "type": item.type,
        "title": item.title,
        "due_in_days": int(item.due_in_days)
    }

    if item.type == "assignment":
        assignments.append(doc)
    elif item.type == "exam":
        exams.append(doc)
    else:
        events.append(doc)

    # Persist immediately (NEW)
    save_data(assignments, exams, events)

class IngestResponse(BaseModel):
    status: str
    message: str

def refresh_from_disk():
    data = load_data()

    assignments.clear()
    exams.clear()
    events.clear()

    assignments.extend(data["assignments"])
    exams.extend(data["exams"])
    events.extend(data["events"])
