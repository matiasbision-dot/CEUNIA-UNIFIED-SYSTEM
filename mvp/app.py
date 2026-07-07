
 + Meta Observer + Evolution
"""

from core.router import ceunia_router
from core.validator import validate
from core.memory import save, get_memory
from core.meta_observer import observe
from core.evolution import evolve


class CEUNIA_MVP:

    def __init__(self):
        self.version = "MVP v1.0"

    def run(self, task, task_type="general"):

        # 1. Selección de ruta
        model = ceunia_router(task_type)

        # 2. Validación inicial
        validation = validate(task)

        # 3. Registro en memoria
        memory_record = {
            "task": task,
            "model": model,
            "validation": validation
        }

        save(memory_record)

        # 4. Observación
        observation = observe(memory_record)

        # 5. Evolución
        evolution = evolve(
            observation,
            validation
        )

        return {
            "model": model,
            "validation": validation,
            "observation": observation,
            "evolution": evolution
        }


if __name__ == "__main__":

    ceunia = CEUNIA_MVP()

    result = ceunia.run(
        "Primera prueba evolutiva CEUNIA",
        "analysis"
    )

    print("=== CEUNIA MVP ===")
    print(result)
    print("=== MEMORY ===")
    print(get_memory())
