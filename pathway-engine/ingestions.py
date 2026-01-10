from pydantic import BaseModel, Field
from typing import Literal
from storage import load_data, save_data

# Initial load from disk into memory
_data = load_data()
assignments = _data["assignments"]
exams = _data["exams"]
events = _data["events"]

class IngestItem(BaseModel):
    # Stricter validation prevents bad data from entering the system
    type: Literal["assignment", "exam", "event"]
    title: str = Field(..., min_length=1)
    due_in_days: int = Field(..., ge=0) # Must be 0 or higher

def ingest_item(item: IngestItem):
    """Adds a new item and immediately saves to disk."""
    doc = item.dict()

    if item.type == "assignment":
        assignments.append(doc)
    elif item.type == "exam":
        exams.append(doc)
    else:
        events.append(doc)

    save_data(assignments, exams, events)

def refresh_from_disk():
    """Syncs the in-memory lists with the current JSON file content."""
    data = load_data()
    
    assignments.clear()
    exams.clear()
    events.clear()

    assignments.extend(data["assignments"])
    exams.extend(data["exams"])
    events.extend(data["events"])