# CEUNIA Omega MIP v0.2 — Integration plan

This branch preserves the existing MVP and historical notebooks unchanged.

## Scope
- Deterministic routing to explicitly registered executors.
- Structural output validation with stated limitations.
- Meta-observation of execution metadata.
- Evolution recommendations without self-modifying policies.
- SQLite event records linked by SHA-256.
- Explicit approval gates for tasks marked as requiring authorization.

## Boundaries
- No provider is assumed available; register an executor explicitly.
- Non-empty output does not prove correctness or task success.
- Hash chaining detects event tampering but does not prove authorship, wall-clock time, or truth.
- Logs store task/output hashes by default, not raw content.
- This is not yet an MCP server, continuous learning system, or production security certification.

## Validation
Run `python -m unittest discover -s tests -v`.

Next: task-specific evaluators, controlled baselines, schema migration, retention controls, and MCP adapters with explicit tool contracts.