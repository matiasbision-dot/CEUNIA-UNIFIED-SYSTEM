# CEUNIA-E / CEUNIA-OBS metacode v0.1

## Purpose
Executable proof-of-mechanism for recursive online learning, bounded update decisions, metric proxies, and hash-chained event provenance.

## CEUNIA metrics in this prototype
- **Potency proxy:** recent-window baseline log-loss minus CEUNIA prequential log-loss.
- **Metapotency proxy:** change in the potency proxy compared with the previous window.
- **Serendipity proxy:** positive per-case gain on a low-confidence expert ensemble case.
- **Meta-serendipity proxy:** serendipity proxy coincident with a context shift proxy.
- **Punto Albedrío:** bounded update gate; a prediction must be emitted before its label can authorize learning.
- **Recursive/autonomous learning:** after each label is revealed, online experts and expert weights update without an external retraining job.
- **Real-time observation:** each prediction/update event is recorded as it occurs.
- **TOE/CER-like provenance:** ordered SHA-256 hash chain; it detects changes to chained event contents, but does not prove the truth of the input data.

## Execution
```bash
python experiments/ceunia_e_metacode_v01.py
```

No third-party dependencies. Three fixed seeds, 2,400 synthetic observations per seed. The target relationship reverses halfway through each stream.

## Important limitations
1. **Synthetic data only.** This does not establish performance on real-world data or future unseen data.
2. The CEUNIA-specific metrics are **experimental proxies**, not validated or certified measures.
3. The Point Albedrío gate in v0.1 only enforces prediction-before-label-update; it is not a full policy, safety, or authorization engine.
4. Hash chaining is not a digital signature and cannot establish source authenticity by itself.
5. This prototype does not demonstrate consciousness, universal autonomy, or general predictive superiority.
6. A fixed 0.5 predictor is a weak reference for this synthetic task; future evaluations must include competitive online baselines, ablations, confidence intervals, and an untouched chronological holdout.

## Acceptance criteria
- Reproducible synthetic stream from fixed seeds.
- Target is not used before prediction.
- Online update occurs only after target reveal.
- Hash chain verifies.
- Report preserves negative outcomes rather than selecting only favorable runs.

## Next experiment
Compare against (a) fixed 0.5, (b) last-outcome baseline, (c) single online logistic model, and (d) adaptive ensemble without CEUNIA metric gates. Then run a frozen walk-forward evaluation on a real dataset, with exact timestamps, data hashes, and no future leakage.
