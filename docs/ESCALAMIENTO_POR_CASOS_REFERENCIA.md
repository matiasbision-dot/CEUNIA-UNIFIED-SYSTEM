# CEUNIA: escalamiento guiado por casos de referencia

Date: 2026-10-12

## Why this change
The existing router selects between models randomly with equal weights. This branch adds an opt-in router that selects only after enough comparable validation/test outcomes have been recorded. It refuses training-set outcomes for routing and falls back to round-robin when evidence is insufficient.

## Historical reference registry
`benchmarks/success_reference_registry.json` captures previously reported CEUNIA experiments as candidate references, not certified findings. Positive, small-effect, synthetic, negative, and inconclusive cases are kept distinct. Values must be reproduced from the source notebook and data before being promoted.

## Scale policy
1. Preserve the existing router and MVP; introduce this router as an opt-in component.
2. Partition by task type, metric, dataset version, and held-out split.
3. Require a minimum sample count before a model can win.
4. Choose direction explicitly (lower error or higher score).
5. Keep an audit event with the selection rationale and sample counts.
6. Never promote based only on training results; use an independent holdout.
7. Keep failed and inconclusive runs in the registry to prevent survivorship bias.

## Next validation
Run unit tests in the repository environment. Then wire a controlled shadow-mode comparison that logs current-router and evidence-router choices without changing production actions. Only after stable, paired results should the routing policy be considered for rollout.
