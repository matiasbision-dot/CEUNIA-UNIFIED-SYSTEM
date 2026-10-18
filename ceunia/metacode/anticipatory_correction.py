"""CEUNIA Ω: anticipatory correction prototype.

This is a causal, one-step-ahead walk-forward experiment on synthetic data.
At each t, predictions are made using only observations with index < t.
Only after prediction is the target revealed and used to update residual bias.
It is NOT a NASA dataset, a real-world forecast, or proof of future performance.
"""
from __future__ import annotations
import hashlib
import json
import math
import random
from typing import Any


def make_synthetic_history(n: int = 1200, seed: int = 20261018) -> list[float]:
    """Deterministic synthetic series with a regime change at 2/3 of the history."""
    rng = random.Random(seed)
    values = []
    for t in range(n):
        slope = 0.025 if t < (2 * n // 3) else -0.018
        y = (
            10
            + slope * t
            + 1.8 * math.sin(2 * math.pi * t / 48)
            + 0.7 * math.sin(2 * math.pi * t / 13)
            + rng.gauss(0, 0.45)
        )
        values.append(y)
    return values


def _mae(actual: list[float], predicted: list[float]) -> float:
    return sum(abs(y - p) for y, p in zip(actual, predicted)) / len(actual)


def walk_forward(
    values: list[float],
    start: int = 100,
    window: int = 64,
    alpha: float = 0.03,
) -> dict[str, Any]:
    """Predict first, reveal target second, update residual correction third."""
    if not (2 <= window <= start < len(values)):
        raise ValueError("Requiere 2 <= window <= start < len(values)")
    if not (0.0 < alpha <= 1.0):
        raise ValueError("alpha debe estar en (0, 1]")
    baseline_preds: list[float] = []
    raw_preds: list[float] = []
    adaptive_preds: list[float] = []
    actuals: list[float] = []
    bias = 0.0

    for t in range(start, len(values)):
        past = values[:t]  # strict causal boundary; target is not in past
        baseline = past[-1]  # persistence baseline
        recent = past[-window:]
        xs = list(range(len(recent)))
        x_mean = sum(xs) / len(xs)
        y_mean = sum(recent) / len(recent)
        denom = sum((x - x_mean) ** 2 for x in xs)
        slope = (
            sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, recent)) / denom
            if denom else 0.0
        )
        raw = recent[-1] + slope
        corrected = raw + bias

        # Lock predictions before revealing the target.
        baseline_preds.append(baseline)
        raw_preds.append(raw)
        adaptive_preds.append(corrected)
        target = values[t]
        actuals.append(target)

        # Update only after target has been revealed and scored.
        residual = target - raw
        bias = (1.0 - alpha) * bias + alpha * residual

    baseline_mae = _mae(actuals, baseline_preds)
    raw_mae = _mae(actuals, raw_preds)
    adaptive_mae = _mae(actuals, adaptive_preds)
    payload = {
        "schema": "CEUNIA-ANTICIPATORY-CORRECTION-1.0",
        "data_kind": "SYNTHETIC_NOT_REAL_WORLD",
        "n_total": len(values),
        "n_test": len(actuals),
        "start_index": start,
        "window": window,
        "alpha": alpha,
        "baseline_mae": baseline_mae,
        "raw_trend_mae": raw_mae,
        "adaptive_mae": adaptive_mae,
        "adaptive_vs_baseline_improvement_pct": 100.0 * (baseline_mae - adaptive_mae) / baseline_mae,
        "adaptive_vs_raw_improvement_pct": 100.0 * (raw_mae - adaptive_mae) / raw_mae if raw_mae else None,
        "bias_final": bias,
        "protocol": "predict -> score/reveal target -> update correction",
        "limitations": [
            "Synthetic series only; no NASA or live data.",
            "Hyperparameters are not tuned on the held-out test segment.",
            "One synthetic regime change does not establish generalization.",
            "Adaptive correction can worsen accuracy and must be compared to baseline.",
        ],
    }
    payload["result_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return payload


if __name__ == "__main__":
    print(json.dumps(walk_forward(make_synthetic_history()), indent=2))
