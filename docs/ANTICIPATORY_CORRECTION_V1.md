# CEUNIA Ω: anticipatory correction v1.1

## Diagnosis
The v1 fixed residual correction used a constant learning rate and applied corrections even though the trend candidate performed worse than the persistence baseline on the deterministic synthetic reference series. The correction lacked an evidence gate.

## Fix
- Persistence is the safe default.
- Predictions use only observations available before each target.
- Candidate selection uses trailing prequential errors from prior observations only.
- A candidate must beat baseline validation MAE by at least the configured margin (default 3%) before it can replace the baseline.
- The current target is revealed only after predictions are stored; then residual bias is updated.
- Reports include all MAEs, selection counts, protocol and SHA-256 fingerprint.

## Run
```bash
python -m unittest discover -s tests -p "test_anticipatory_correction.py" -v
python -m ceunia.metacode.anticipatory_correction
```

## Evidence boundary
This run uses deterministic synthetic data, not NASA POWER or live data. A no-switch result means the gate rejected unproven corrections; it is not evidence of predictive superiority. Validate with a hashed real dataset, chronological train/validation/test splits, frozen parameters and all results reported. Not for financial execution.
