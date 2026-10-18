# CEUNIA Ω: anticipatory correction prototype v1

This module tests a causal version of the proposed anticipatory-correction loop.

1. Construct a forecast using only historical observations available before time t.
2. Record the forecast before revealing the target.
3. Reveal the target, score the forecast, and only then update residual correction.
4. Compare persistence baseline, raw trend, and adaptive correction on the same test rows.
5. Emit a SHA-256 fingerprint of the report for traceability.

## Run

```bash
python -m unittest discover -s tests -v
python -m ceunia.metacode.anticipatory_correction
```

## Evidence boundary

The included stream is deterministic synthetic data with a regime change, not NASA POWER or live data. Results validate implementation behavior only, not real-world predictive advantage. The adaptive correction may underperform the baseline; that outcome must be reported rather than hidden. Do not use this prototype for financial execution.

## Next validation

Replace the synthetic generator with an immutable, hashed historical dataset; define the target and forecast horizon; preserve chronological splits; tune only on a pre-test validation window; then run the frozen configuration once on a held-out test window and publish all metrics, errors, and hashes.
