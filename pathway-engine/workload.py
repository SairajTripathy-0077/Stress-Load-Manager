# workload.py

from ingestions import assignments, exams, events

def compute_workload_index():
    return len(assignments) + 2 * len(exams) + len(events)

def detect_stress(load: int):
    if load <= 2:
        return "Low"
    elif load <= 4:
        return "Medium"
    else:
        return "High"
