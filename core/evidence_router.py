"""Evidence-based model routing for CEUNIA.

Uses only comparable, observed evaluation records. If evidence is insufficient,
routing falls back to deterministic round-robin rather than claiming a winner.
"""
from collections import defaultdict
from datetime import datetime, timezone
from math import isfinite
from typing import Dict, Iterable, Optional


class EvidenceRouter:
    def __init__(self, models=("openai", "claude"), min_samples=20):
        if not models:
            raise ValueError("models must not be empty")
        if min_samples < 1:
            raise ValueError("min_samples must be >= 1")
        self.models = tuple(models)
        self.min_samples = min_samples
        self._scores = defaultdict(list)
        self._cursor = 0
        self.history = []

    def record_result(self, *, model, task_type, metric, value, dataset_id, split="validation"):
        if model not in self.models:
            raise ValueError("unknown model")
        if not task_type or not metric or not dataset_id:
            raise ValueError("task_type, metric, and dataset_id are required")
        if split not in ("validation", "test"):
            raise ValueError("training-set results cannot drive routing")
        if not isinstance(value, (int, float)) or not isfinite(float(value)):
            raise ValueError("metric value must be finite numeric")
        key = (str(task_type), str(metric), str(dataset_id), str(split), model)
        self._scores[key].append(float(value))

    def select_model(self, task_type="general", metric="loss", dataset_id="default", split="validation", lower_is_better=True):
        comparable = {}
        for model in self.models:
            values = self._scores.get((str(task_type), str(metric), str(dataset_id), str(split), model), [])
            if len(values) >= self.min_samples:
                comparable[model] = sum(values) / len(values)

        if comparable:
            best_value = min(comparable.values()) if lower_is_better else max(comparable.values())
            winners = sorted(model for model, value in comparable.items() if value == best_value)
            selected = winners[0]
            reason = "best_mean_on_comparable_held_out_results"
        else:
            selected = self.models[self._cursor % len(self.models)]
            self._cursor += 1
            reason = "insufficient_comparable_evidence_round_robin_fallback"

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": str(task_type),
            "metric": str(metric),
            "dataset_id": str(dataset_id),
            "split": split,
            "selected_model": selected,
            "reason": reason,
            "sample_counts": {
                model: len(self._scores.get((str(task_type), str(metric), str(dataset_id), str(split), model), []))
                for model in self.models
            },
        }
        self.history.append(event)
        return selected

    def get_history(self):
        return list(self.history)
