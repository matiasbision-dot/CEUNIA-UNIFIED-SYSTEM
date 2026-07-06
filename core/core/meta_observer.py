"""
CEUNIA Meta Observer

Version: 1.0
Purpose:
Observes system behavior across time to detect drift, inconsistency and evolution patterns.
This is the first layer of self-referential evaluation.
"""

class CEUNIAMetaObserver:

def __init__(self):
    self.drift_history = []

def analyze_memory(self, memory_store):
    """
    Evaluates system-level behavior patterns.
    """

    if not memory_store:
        return {
            "status": "empty",
            "drift": 0.0,
            "coherence_trend": "stable"
        }

    validations = [
        item.get("validation", {}).get("coherence", 0)
        for item in memory_store
    ]

    avg_coherence = sum(validations) / len(validations)

    # simple drift estimation
    drift = max(validations) - min(validations)

    if avg_coherence > 0.75:
        trend = "stable"
    elif avg_coherence > 0.5:
        trend = "moderate"
    else:
        trend = "unstable"

    report = {
        "average_coherence": round(avg_coherence, 2),
        "drift": round(drift, 2),
        "trend": trend
    }

    self.drift_history.append(report)

    return report

def history(self):
    return self.drift_history
