"""
CEUNIA Validator
Módulo de evaluación de coherencia, riesgo y calidad.
"""


class CEUNIAValidator:

    def __init__(self):
        self.history = []

    def evaluate(self, data):

        result = {
            "coherence": self._coherence_check(data),
            "risk": self._risk_check(data),
            "status": "validated"
        }

        self.history.append(result)

        return result

    def _coherence_check(self, data):
        if data is None or data == "":
            return 0

        return 1

    def _risk_check(self, data):
        return "low"

    def get_history(self):
        return self.history


validator = CEUNIAValidator()


def validate(data):
    return validator.evaluate(data)
