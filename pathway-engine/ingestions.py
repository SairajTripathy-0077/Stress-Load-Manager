from pydantic import BaseModel
from typing import Literal

# In-memory store
assignments = []
exams = []
events = []

class IngestItem(BaseModel):
    type: Literal["assignment", "exam", "event"]
    title: str
    due_in_days: int

def ingest_item(item: IngestItem):
    if item.type == "assignment":
        assignments.append(item)
    elif item.type == "exam":
        exams.append(item)
    else:
        events.append(item)

class IngestResponse(BaseModel):
    status: str
    message: str
