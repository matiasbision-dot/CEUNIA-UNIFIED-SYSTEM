# ALL I + ONECLICK: economía de datos vivos

**CEUNIA Ω architecture note | v0.1 | 14 November 2026**

## 1. Product thesis

ONECLICK is the universal intent-to-resolution interface: one concise human intention becomes a verified, reviewable and, only with authorization, executable resolution.

ALL I is the proposed integral-intelligence layer: it interprets context, coordinates authorized data sources and capabilities, evaluates evidence and routes work toward a useful result. CEUNIA Ω supplies meta-observation, memory, coherence controls and recursive learning.

**Living-data economy:** economic value is created when timely, permissioned, provenance-bearing information materially improves a resolution. The unit of value is not raw data volume; it is a verified contribution to an outcome.

## 2. System roles

| Layer | Responsibility |
|---|---|
| ALL I | Contextual interpretation, source coordination, capability routing and resolution orchestration |
| CEUNIA Ω | Meta-observation, memory, evaluation, coherence, risk and learning |
| ONECLICK | Minimal-expression interface for intent, proposal, confirmation and authorized action |
| Living-data economy | Value model for permitted, current, useful information and measured outcomes |

These are complementary layers, not competing products.

## 3. Live-data record contract

Every observation entering a resolution should carry:

- source identity and source type;
- observation timestamp and expiry;
- declared purpose and permission scope;
- permission status supplied by an authoritative consent or contract mechanism;
- quality score and validation method;
- value, unit and relevant context reference;
- stable content-derived identity for traceability.

An observation is admissible only if permission is present, requested purpose matches the declared scope, the observation is current, timestamps are valid and quality meets the configured threshold. Failure is closed: ask, refresh, or abstain.

## 4. Real-time interpretation loop

1. Capture an explicit intent.
2. Resolve only unambiguous slots; ask about missing or conflicting details.
3. Identify which live observations are necessary for this purpose.
4. Obtain them from authorized sources; validate provenance, permission, freshness and quality.
5. Compare options and expose uncertainty, total cost and trade-offs.
6. Present a reviewable proposal.
7. Require human confirmation for consequential action.
8. Record the external response and measured outcome.
9. Evaluate what improved the resolution; update memory under its own permissions and retention rules.

## 5. Economic model

Potential value dimensions include:

- **Resolution utility:** did the information help complete the intended task?
- **Freshness:** was it current at the decision time?
- **Reliability:** was it accurate and independently verifiable?
- **Efficiency:** did it reduce time, steps, errors or total cost?
- **Outcome evidence:** did a real provider or user outcome confirm the contribution?

No economic value should be booked merely because data was collected, inferred, cached or displayed. Value attribution requires a defined baseline, measured outcome, source lineage and a method that avoids double counting. Revenue sharing or data licensing requires separate legal terms and explicit permissions.

## 6. Governance and non-negotiable boundaries

- Data minimization: collect only what the declared resolution requires.
- Purpose limitation: permission for one use is not blanket permission for another.
- Provenance: never label fixtures, estimates or stale cache as live evidence.
- Human agency: inferred preferences do not silently become order instructions.
- Security: secrets and payment credentials do not belong in evidence records.
- Retention: define expiry, deletion, access control, backup and audit policy before production.
- Execution: confirmation, merchant acceptance, payment and fulfillment are distinct events.
- Learning: use outcomes only within their authorized purpose; provide correction and review paths.

## 7. Current implementation evidence

Implemented in this repository:

- `core/intent.py`: conservative Spanish intent extraction;
- `core/catalog.py`: catalog snapshot, provenance and freshness checks;
- `core/proposal.py`: deterministic review proposal;
- `core/confirmation.py`: explicit human decision;
- `core/confirmation_store.py`: SQLite proposal, decision and outcome ledger;
- `core/merchant_adapter.py`: guarded adapter boundary, denied by default;
- `core/live_data.py`: permission, purpose, freshness and quality admissibility contract;
- `examples/live_data_economy.py`: local fixture demonstration, no external data fetch.

## 8. Not yet implemented

- production ingestion connectors or continuous event streams;
- a live merchant with written authorization and verified API access;
- production consent management and identity/access controls;
- production-grade encrypted storage, retention/deletion workflows and backups;
- economic attribution, billing, revenue-sharing or data marketplace;
- autonomous learning from real outcomes.

The current live-data module validates records supplied to it. It does not fetch external data, establish legal consent, sell data or prove a commercial transaction.

## 9. First commercial validation

Choose one authorized source and one narrow resolution. For example: obtain a merchant catalog and availability snapshot, verify its source and validity, resolve one explicit order intent, present a priced proposal, obtain human confirmation, submit through an authorized idempotent adapter, then reconcile the merchant response and receipt. Measure time, error rate, completion rate and price accuracy against a documented baseline.

**North-star principle:** maximum resolution with minimum expression, while preserving provenance, permission, human agency and measurable evidence.