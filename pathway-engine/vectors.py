# vectors.py

def explain_workload(load, stress, streams):
    return (
        f"Your workload index is {load}, indicating {stress} stress. "
        f"You currently have {streams['assignments']} assignments, "
        f"{streams['exams']} exams, and "
        f"{streams['events']} events. "
        f"Consider prioritizing urgent tasks to reduce stress."
    )
