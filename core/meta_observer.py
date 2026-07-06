"""
CEUNIA Meta Observer
Capa de observación del comportamiento del sistema.
"""


class CEUNIAMetaObserver:

    def __init__(self):
        self.events = []

    def observe(self, state):
        event = {
            "state": state,
            "type": "observation"
        }

        self.events.append(event)

        return event

    def detect_change(self, previous, current):

        if previous != current:
            return {
                "change_detected": True,
                "previous": previous,
                "current": current
            }

        return {
            "change_detected": False
        }

    def history(self):
        return self.events


observer = CEUNIAMetaObserver()


def observe(state):
    return observer.observe(state)
