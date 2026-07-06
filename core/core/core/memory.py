"""
CEUNIA Core Memory

Version: 1.0
Purpose:
Stores system interactions for future adaptation and evolution.
"""

import json
from datetime import datetime

class CEUNIAMemory:

def __init__(self):
    self.store = []

def add(self, input_text, output, validation):
    """
    Stores a single interaction.
    """
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": input_text,
        "output": output,
        "validation": validation
    }

    self.store.append(record)
    return record

def get_all(self):
    return self.store

def get_last(self, n=5):
    return self.store[-n:]
