"""
CEUNIA MVP
Sistema mínimo de decisión, validación y memoria.
"""

from core.router import ceunia_router


class CEUNIA_MVP:

    def __init__(self):
        self.memory = []
        self.version = "MVP v1.0"

    def run(self, task, task_type="general"):
        model = ceunia_router(task_type)

        result = {
            "task": task,
            "selected_model": model,
            "status": "processed"
        }

        self.memory.append(result)

        return result

    def get_memory(self):
        return self.memory


if __name__ == "__main__":

    ceunia = CEUNIA_MVP()

    response = ceunia.run(
        "Evaluar primera decisión CEUNIA",
        "analysis"
    )

    print("=== CEUNIA MVP ===")
    print(response)
