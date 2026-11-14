# ONECLICK Economic Trial Contract v1.0

**Purpose:** measure whether one authorized, real-world resolution produces better outcomes than a documented baseline. This contract is a measurement specification, not evidence that a pilot has already happened.

## Scope

One trial = one explicit user intent, one declared purpose, one authorized data source (or a clearly enumerated set), one comparable baseline, one ONECLICK resolution, and one independently traceable outcome.

The trial must distinguish:
- **CI evidence:** code and validation behavior using fixtures.
- **Pilot evidence:** timestamps, source records, merchant response, receipt and outcome from a real authorized operation.

Fixture results must never be presented as pilot results.

## Five required dimensions

| Metric | Formula / evidence | Interpretation |
|---|---|---|
| Time saved | baseline elapsed seconds − ONECLICK elapsed seconds | Positive saves time; negative means slower |
| Errors avoided | baseline error count − ONECLICK error count | Positive avoids errors; negative means more errors |
| Price/result improvement | baseline comparable total − ONECLICK comparable total, same currency | Positive is cheaper; negative is more expensive |
| Source contribution | distinct source IDs, live-data record IDs and contribution evidence references | Shows which permitted source actually informed the resolution |
| Value distribution | status: not defined / terms authorized / reconciled, plus terms reference | No allocation or sharing is implied without valid, explicit terms |

### Measurement rules

1. Use the same intent, scope, fulfillment mode, quantity and comparable basket for baseline and ONECLICK.
2. Record start/end timestamps using a consistent clock and define whether human waiting time is included.
3. Count only errors under a written taxonomy. Apply the same taxonomy to baseline and ONECLICK.
4. Compare final comparable totals, not catalog-only subtotals. Include delivery, fees, discounts and taxes where applicable. If a final total is unavailable, mark price improvement as not measured rather than substituting a partial price.
5. A source contribution requires a source identifier, the corresponding live-data record identity and evidence of how it contributed. Merely querying or displaying a source is not sufficient.
6. Mark outcome verified only when there is an authoritative outcome reference, such as a merchant acceptance plus receipt or equivalent fulfillment evidence. A proposal, confirmation screen or local fixture is not an external outcome.
7. Do not monetize saved time or avoided errors until a separately justified valuation method is approved. Report seconds and counts first.
8. Do not invent revenue shares or percentages. Distribution remains not defined until explicit terms, authority and participant permissions exist. Reconciliation requires verified outcome evidence.

## Pass / fail gates

- Missing permission, purpose mismatch, stale source or insufficient quality: reject or abstain.
- Ambiguous intent or fulfillment: ask; do not silently infer.
- No comparable baseline: report the missing metric; do not claim improvement.
- No authoritative outcome evidence: outcome remains unverified.
- No valid distribution terms: no value-sharing claim or transfer.
- Duplicate source attribution: reject.
- Any fixture-only run: CI demonstration only, never a commercial result.

## Implementation

- `core/economic_trial.py`: immutable measurement contract and derived metrics.
- `tests/test_economic_trial.py`: validation and negative-case coverage.
- `examples/economic_trial_contract.py`: fixture-only CI demonstration.
- `.github/workflows/ceunia-core-tests.yml`: executes the demonstration and test discovery.

## Current status

The contract and CI example are implemented in the repository. A real merchant pilot is **not yet evidenced**. It still requires one merchant's written authorization, verified catalog/availability access, an approved purpose and data scope, a real baseline, and a real outcome/receipt. The code does not itself create consent, connect to a merchant, submit an order or process payment.

**North star:** maximum resolution with minimum expression, measured without confusing simulated evidence with real economic value.
