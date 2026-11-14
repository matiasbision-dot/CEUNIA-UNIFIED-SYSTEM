"""Local contract example; all values are illustrative fixtures, not pilot evidence."""
from decimal import Decimal
from core.economic_trial import EconomicTrial, SourceContribution

trial = EconomicTrial(
    trial_id="fixture-only-001",
    resolution_id="fixture-resolution-001",
    baseline_time_seconds=600,
    oneclick_time_seconds=90,
    baseline_error_count=2,
    oneclick_error_count=0,
    baseline_total=Decimal("12000"),
    oneclick_total=Decimal("10500"),
    currency="ARS",
    outcome_status="fixture_only",
    outcome_evidence_ref="fixture://not-a-merchant-receipt",
    source_contributions=(
        SourceContribution("fixture_catalog", "fixture-record-id", "fixture://catalog-snapshot"),
    ),
)
print("FIXTURE ONLY - NOT A REAL ECONOMIC RESULT")
print(trial.metrics())
