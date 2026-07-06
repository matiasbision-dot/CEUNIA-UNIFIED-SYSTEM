"""
CEUNIA Core Router

Version: 1.0
Purpose:
Coordinates the routing of tasks across AI models and future CEUNIA engines.
"""

import random
from datetime import datetime

AVAILABLE_MODELS = {
"openai": {
"weight": 1.0,
"status": "active"
},
"claude": {
"weight": 1.0,
"status": "active"
}
}

class CEUNIARouter:

def __init__(self):
    self.history = []

def available_models(self):
    return [
        name
        for name, info in AVAILABLE_MODELS.items()
        if info["status"] == "active"
    ]

def select_model(self, task_type="general"):

    models = self.available_models()

    if not models:
        raise RuntimeError("No models available.")

    weights = [
        AVAILABLE_MODELS[m]["weight"]
        for m in models
    ]

    selected = random.choices(
        models,
        weights=weights,
        k=1
    )[0]

    self.history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "task": task_type,
        "selected": selected
    })

    return selected

def routing_history(self):
    return self.history

router = CEUNIARouter()

def ceunia_router(task_type="general"):
"""
Public router interface.
"""
return router.select_model(task_type)
