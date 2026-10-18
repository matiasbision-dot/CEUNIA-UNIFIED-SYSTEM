"""CEUNIA Ω real-data walk-forward validation using NASA POWER monthly T2M.

Forecast target: monthly mean 2 m air temperature (T2M) for a fixed point near
Mar del Plata, Argentina. Historical months are treated as simulated future:
predict month m using data through m-1, lock forecast, then reveal m and update
the residual correction. No future target values are used to make that month's
forecast. This is a research prototype, not an operational weather forecast.
"""
from __future__ import annotations
import hashlib, json, math, os, urllib.parse, urllib.request
from datetime import date
from typing import Any

LATITUDE = -38.0
LONGITUDE = -57.55
START_DATE = "20100101"
END_DATE = "20251231"
PARAMETER = "T2M"
USER_AGENT = "CEUNIA-Research-Prototype/1.0"

def fetch_nasa_power_monthly() -> tuple[list[str], list[float], str]:
    params = {
        "parameters": PARAMETER, "community": "RE",
        "longitude": str(LONGITUDE), "latitude": str(LATITUDE),
        "start": START_DATE, "end": END_DATE, "format": "JSON",
    }
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        raw = response.read()
    digest = hashlib.sha256(raw).hexdigest()
    payload = json.loads(raw)
    properties = payload.get("properties", {})
    parameter_data = properties.get("parameter", {}).get(PARAMETER)
    if not isinstance(parameter_data, dict) or not parameter_data:
        raise RuntimeError("NASA POWER response lacks monthly T2M parameter")
    # Monthly endpoint keys are YYYYMM; skip NASA's missing-data sentinel.
    pairs = []
    for key, value in sorted(parameter_data.items()):
        if not (isinstance(key, str) and len(key) == 6 and key.isdigit()):
            continue
        val = float(value)
        if not math.isfinite(val) or val <= -900:
            continue
        pairs.append((f"{key[:4]}-{key[4:6]}", val))
    if len(pairs) < 100:
        raise RuntimeError(f"Too few valid monthly observations: {len(pairs)}")
    return [p[0] for p in pairs], [p[1] for p in pairs], digest

def mae(actual: list[float], predicted: list[float]) -> float:
    if not actual or len(actual) != len(predicted):
        raise ValueError("Series must have equal non-zero lengths")
    return sum(abs(a-p) for a,p in zip(actual,predicted))/len(actual)

def run_walk_forward(months: list[str], values: list[float], initial_train: int = 60,
                     validation_window: int = 24, alpha: float = 0.15,
                     min_improvement: float = 0.02) -> dict[str, Any]:
    if len(months) != len(values) or initial_train < 24 or initial_train >= len(values):
        raise ValueError("Invalid chronological series or initial_train")
    if validation_window < 12 or not 0 < alpha <= 1 or not 0 <= min_improvement < 1:
        raise ValueError("Invalid validation_window, alpha, or min_improvement")
    base, seasonal, corrected, gated, actuals = [], [], [], [], []
    dates = []
    residual_bias = 0.0
    # Every forecast is created before the current month's target is read.
    for t in range(initial_train, len(values)):
        past = values[:t]
        pred_base = past[-1]  # last-month persistence
        pred_seasonal = values[t-12] if t >= 12 else pred_base
        pred_corrected = pred_seasonal + residual_bias
        # Selection uses only outcomes from prior months whose forecasts are already scored.
        selected = pred_base
        if len(actuals) >= validation_window:
            recent_actual = actuals[-validation_window:]
            scores_base = mae(recent_actual, base[-validation_window:])
            scores_seasonal = mae(recent_actual, seasonal[-validation_window:])
            scores_corrected = mae(recent_actual, corrected[-validation_window:])
            candidate_scores = [(scores_seasonal, pred_seasonal),
                                (scores_corrected, pred_corrected)]
            best_score, best_prediction = min(candidate_scores, key=lambda x: x[0])
            if best_score < scores_base * (1.0 - min_improvement):
                selected = best_prediction
        # Lock predictions, then reveal this month's actual value.
        base.append(pred_base); seasonal.append(pred_seasonal)
        corrected.append(pred_corrected); gated.append(selected)
        actual = values[t]
        actuals.append(actual); dates.append(months[t])
        residual_bias = (1.0-alpha)*residual_bias + alpha*(actual-pred_seasonal)
    return {
        "initial_train_months": initial_train,
        "test_months": len(actuals),
        "test_start": dates[0],
        "test_end": dates[-1],
        "baseline_persistence_mae": mae(actuals, base),
        "seasonal_naive_mae": mae(actuals, seasonal),
        "adaptive_seasonal_correction_mae": mae(actuals, corrected),
        "evidence_gated_mae": mae(actuals, gated),
        "gated_vs_baseline_improvement_pct": 100*(mae(actuals,base)-mae(actuals,gated))/mae(actuals,base),
        "selection_counts": {
            "baseline": sum(abs(g-b)<1e-12 for g,b in zip(gated,base)),
            "seasonal_or_corrected": sum(abs(g-b)>=1e-12 for g,b in zip(gated,base)),
        },
        "protocol": "forecast using months < t -> lock -> reveal month t -> score -> update residual",
        "warning": "Historical replay with sequential reveal; not proof of future accuracy or climate attribution.",
    }

def main() -> dict[str, Any]:
    months, values, source_hash = fetch_nasa_power_monthly()
    report = {
        "schema": "CEUNIA-NASA-POWER-WALK-FORWARD-1.0",
        "dataset": "NASA POWER monthly point data",
        "parameter": PARAMETER,
        "units": "degC",
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "source_period_requested": f"{START_DATE}-{END_DATE}",
        "observations": len(values),
        "first_month": months[0],
        "last_month": months[-1],
        "raw_response_sha256": source_hash,
        "method": run_walk_forward(months, values),
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["report_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    output = os.environ.get("CEUNIA_REPORT_PATH", "ceunia_nasa_power_report.json")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    main()
