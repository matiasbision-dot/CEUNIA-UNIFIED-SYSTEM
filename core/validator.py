class Validator:
    def __init__(self, threshold=0.70):
        self.threshold = threshold

    def validate(self, score):
        """
        Valida si un puntaje supera el umbral mínimo.
        """
        return score >= self.threshold

    def validate_decision(self, decision):
        """
        Verifica que la decisión tenga los campos mínimos.
        """
        required = ["score", "action"]

        for field in required:
            if field not in decision:
                return False

        return self.validate(decision["score"])
