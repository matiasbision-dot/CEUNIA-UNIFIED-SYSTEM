# CEUNIA-E PACR v0.2

## Correct terminology
CEUNIA-native variables in this version are **Potercia** and **Metapotercia**. Do not rename them to potencia/metapotencia.

- **Potercia (provisional):** rolling 50-case reduction in log-loss versus a sequential last-observed-outcome baseline.
- **Metapotercia (provisional):** change in Potercia compared with the preceding non-overlapping window.
- **Punto Albedrío:** bounded decision gate that allows learning only after the current forecast is committed and the outcome is revealed.
- **Recursive online learning:** update expert parameters and ensemble weights after every revealed outcome.
- **TOE/CER-like trace:** each forecast and update is recorded in a SHA-256 chained event sequence.

## Run
```bash
python experiments/ceunia_e_metacode_v02.py
```
Standard library only. Three fixed seeds, 2,400 synthetic observations per seed. A simulated concept reversal occurs halfway through the stream.

## Latest execution
See `results/ceunia_e_metacode_v02_synthetic_report.json`. All three event chains verified and each current outcome was kept out of its preceding forecast. Mean log-loss was 0.4654 versus 0.8324 for the sequential last-outcome comparator.

## Limitations
Synthetic-only, weak comparator, no real-time external data, no production autonomy, and no claim of universal or real-world predictive superiority. Error rose in the second half after the concept reversal. Potercia and Metapotercia are provisional operational proxies, not certified metrics. Hash chaining does not prove the truth or authenticity of source data.

## Next
Compare against a single online logistic model and a tuned adaptive ensemble; add ablations for the update policy; then run a frozen chronological holdout on real data with no future leakage.
