# CEUNIA Ω | 99 Triads Runtime Bridge

A dependency-free bridge between the named 99-triad registry and CEUNIA's mission/evaluation layer.

## Safety and status

- Default behavior validates the registry and generates a JSONL dispatch plan.
- It does **not** call models, launch autonomous agents, or claim missions were executed.
- Live execution requires an explicitly supplied executor adapter to `execute_with_adapter()`.
- Returned results must be checked against acceptance criteria before being recorded as successful.
- Punto Albedrío remains a human-review gate for irreversible or high-impact actions.

## Run

```bash
python ceunia/triads/runtime.py --registry data/CEUNIA_99_Triadas_Nombradas.csv --output artifacts/ceunia_triads_dispatch.jsonl
```

Pilot only the first three:

```bash
python ceunia/triads/runtime.py --registry data/CEUNIA_99_Triadas_Nombradas.csv --limit 3 --output artifacts/pilot_dispatch.jsonl
```

The command emits a JSON report beside the JSONL plan with a SHA-256 checksum. This is a local integrity checksum, not an external timestamp, authorship certificate, or independent audit.

## Integration contract

Input: CSV with columns `id_ceunia`, `nombre_triada`, three perspective names, knowledge profile, mission, deliverable, evolutionary criteria, integration rule, and status. IDs must cover T001..T099.

Output: JSONL work items with stable triad IDs, mission metadata, acceptance criteria, integration rule, and explicit `PLANNED_NOT_EXECUTED` status.

Recommended rollout: validate all 99, execute a supervised pilot of 3, compare outputs against a baseline, inspect positive/neutral/negative evidence, then expand by family. Do not represent historical thinker profiles as literal simulations or verified opinions of those people.
