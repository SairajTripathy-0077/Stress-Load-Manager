import json
import os

DATA_FILE = "data_store.json"

def load_data():
    """Reads data from JSON. Returns a structured dict even if file is missing or broken."""
    if not os.path.exists(DATA_FILE):
        return {"assignments": [], "exams": [], "events": []}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Ensure the required keys always exist
            return {
                "assignments": data.get("assignments", []),
                "exams": data.get("exams", []),
                "events": data.get("events", [])
            }
    except (json.JSONDecodeError, IOError):
        # If file is corrupted, return empty structure
        return {"assignments": [], "exams": [], "events": []}

def save_data(assignments, exams, events):
    """Persists current workload to the JSON file with pretty printing."""
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