# CEUNIA MetaCode Evolution v1

## Purpose
A small, deterministic evidence-routing layer that turns experiment reports into
structured CEUNIA evolution decisions. It preserves favourable results while
tracking their evidentiary state and choosing a proportionate next action.

## What it does
- Computes relative MAE improvement and compares walk-forward to baseline/model.
- Distinguishes reported results from independently reproduced results.
- Emits Punto Albedrío recommendations.
- Creates a JSON CER bundle and SHA-256 fingerprints.
- Keeps financial use in research/shadow mode; it does not place trades.
- Does not claim the 99 triads are running agents unless execution logs establish that.

## Use
```python
from ceunia.metacode.evolution import build_cer_bundle

reports = [{
    "experiment_id": "NASA-POWER-2026-10",
    "domain": "environmental_prediction",
    "baseline_mae": 1.291156186612576,
    "model_mae": 1.1924114948962365,
    "walkforward_mae": 1.1846364064690789,
    "test_n": 493,
    "configurations_passed": 99,
    "configurations_total": 99,
    "source": "NASA POWER, operator-reported",
    "period": ["2020-01-01", "2026-10-14"],
    "source_hashes": [],
    "reproduced": False
}]
print(build_cer_bundle(reports))
```

Add the finance report only when its actual baseline/model metrics and source
metadata are available. Missing metrics cause a clear error rather than being
fabricated.

## Test
Run from repository root:
```bash
python -m unittest discover -s tests -v
```

## Evidence boundary
This is a proposed integration on a feature branch. It does not mean tests have
been run, NASA results have been independently reproduced, finance results exist,
or triads are deployed.
