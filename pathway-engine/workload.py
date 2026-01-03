# workload.py
from datetime import datetime

def compute_workload(assignments, exams, events):
    """
    Returns structured workload intelligence.
    """
    today = datetime.utcnow().date()

    def categorize(items):
        today_items = []
        week_items = []
        later_items = []

        for x in items:
            d = x["due_in_days"]
            if d <= 1:
                today_items.append(x)
            elif d <= 7:
                week_items.append(x)
            else:
                later_items.append(x)

        return today_items, week_items, later_items

    a_today, a_week, a_later = categorize(assignments)
    e_today, e_week, e_later = categorize(exams)
    v_today, v_week, v_later = categorize(events)

    # Simple workload score
    score = (
        len(a_today) * 3 +
        len(e_today) * 4 +
        len(a_week) * 2 +
        len(e_week) * 3 +
        len(v_week)
    )

    stress_level = (
        "high" if score >= 10 else
        "medium" if score >= 5 else
        "low"
    )

    return {
        "score": score,
        "stress_level": stress_level,
        "today": {
            "assignments": a_today,
            "exams": e_today,
            "events": v_today,
        },
        "this_week": {
            "assignments": a_week,
            "exams": e_week,
            "events": v_week,
        },
        "later": {
            "assignments": a_later,
            "exams": e_later,
            "events": v_later,
        }
    }
