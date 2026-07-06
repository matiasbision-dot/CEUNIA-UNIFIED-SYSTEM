"""
CEUNIA Memory
Sistema básico de almacenamiento de estados, resultados y aprendizajes.
"""


class CEUNIAMemory:

    def __init__(self):
        self.records = []

    def store(self, data):
        self.records.append(data)
        return True

    def retrieve_all(self):
        return self.records

    def last(self):
        if len(self.records) == 0:
            return None

        return self.records[-1]

    def clear(self):
        self.records = []


memory = CEUNIAMemory()


def save(data):
    return memory.store(data)


def get_memory():
    return memory.retrieve_all()
