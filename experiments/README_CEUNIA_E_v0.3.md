# CEUNIA-E PACR v0.3: adaptive recovery

## What changed
- Correct CEUNIA-native metric names: **Potercia** and **Metapotercia**.
- Add an online ensemble with a drift-aware variant.
- Drift detection compares rolling 50-case log-loss windows, requires repeated deterioration, applies a 150-step cooldown, resets ensemble weights, and boosts learning rates for 80 updates.
- Compare three models on identical synthetic sequences: single online logistic regression, adaptive ensemble, and drift-aware ensemble.
- 20 fixed seeds × 3,000 observations = 60,000 observations total.
- Hash-chain event integrity is verified for each model run.

## Metrics (provisional)
Potercia = rolling 50-case reduction in log-loss versus the last-observed-outcome baseline.
Metapotercia = change in Potercia relative to the preceding window.
These are operational proxies, not validated universal units.

## Run
```bash
python experiments/ceunia_e_metacode_v03.py
```

## Caveats
Synthetic-only. The concept reversal is preconstructed. Drift thresholds are not tuned on a separate holdout. No real-world predictive advantage is claimed. The event hash chain detects modifications within the chain but does not authenticate source truth. Next step: ablations and a frozen chronological evaluation on genuinely new data.
