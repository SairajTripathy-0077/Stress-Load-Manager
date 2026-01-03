# ingestions.py
from pydantic import BaseModel
from typing import Literal

# In-memory stores as lists of plain dicts (not Pydantic objects)
assignments = []
exams = []
events = []

class IngestItem(BaseModel):
    type: Literal["assignment", "exam", "event"]
    title: str
    due_in_days: int

def ingest_item(item: IngestItem):
    # Convert to plain dict to avoid object repr issues later
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

class IngestResponse(BaseModel):
    status: str
    message: str
