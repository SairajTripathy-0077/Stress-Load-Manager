# storage.py
import json
import os

DATA_FILE = "data_store.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "assignments": [],
            "exams": [],
            "events": []
        }

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Ensure structure always exists
    return {
        "assignments": data.get("assignments", []),
        "exams": data.get("exams", []),
        "events": data.get("events", [])
    }

def save_data(assignments, exams, events):
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "assignments": assignments,
                "exams": exams,
                "events": events
            },
            f,
            indent=2
        )
