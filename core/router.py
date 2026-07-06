
"""
CEUNIA Core Router
Módulo encargado de seleccionar la ruta de procesamiento.
"""

import random
from datetime import datetime


AVAILABLE_MODELS = {
    "openai": 1.0,
    "claude": 1.0
}


class CEUNIARouter:

    def __init__(self):
        self.history = []

    def select_model(self, task_type="general"):
        models = list(AVAILABLE_MODELS.keys())
        weights = list(AVAILABLE_MODELS.values())

        selected = random.choices(
            models,
            weights=weights,
            k=1
        )[0]

        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "task_type": task_type,
            "selected_model": selected
        })

        return selected

    def get_history(self):
        return self.history


router = CEUNIARouter()


def ceunia_router(task_type="general"):
    return router.select_model(task_type)
