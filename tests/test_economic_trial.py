import unittest
from decimal import Decimal
from core.economic_trial import EconomicTrial, SourceContribution


def source(source_id="merchant_catalog"):
    return SourceContribution(source_id, "live-record-sha256", "catalog-snapshot-ref")


def trial(**changes):
    values = dict(
        trial_id="pilot-001", resolution_id="resolution-001",
        baseline_time_seconds=600, oneclick_time_seconds=90,
        baseline_error_count=2, oneclick_error_count=0,
        baseline_total=Decimal("12000"), oneclick_total=Decimal("10500"),
        currency="ARS", outcome_status="verified",
        outcome_evidence_ref="merchant-receipt-001",
        source_contributions=(source(),),
    )
    values.update(changes)
    return EconomicTrial(**values)


class EconomicTrialContractTests(unittest.TestCase):
    def test_measures_all_five_dimensions(self):
        result = trial().metrics()
        self.assertEqual(result["time_saved_seconds"], 510)
        self.assertEqual(result["errors_avoided"], 2)
        self.assertEqual(result["price_improvement"], "1500")
        self.assertEqual(result["source_count"], 1)
        self.assertTrue(result["outcome_verified"])
        self.assertEqual(result["distribution_status"], "not_defined")

    def test_negative_improvement_is_not_hidden(self):
        self.assertEqual(trial(oneclick_total=Decimal("13000")).price_improvement, Decimal("-1000"))

    def test_time_can_be_worse_and_is_reported(self):
        self.assertEqual(trial(oneclick_time_seconds=700).time_saved_seconds, -100)

    def test_error_count_can_increase_and_is_reported(self):
        self.assertEqual(trial(oneclick_error_count=3).errors_avoided, -1)

    def test_unverified_outcome_cannot_claim_verified_value(self):
        result = trial(outcome_status="pending", outcome_evidence_ref="pending-log")
        self.assertFalse(result.economic_claim_is_verified)

    def test_missing_outcome_evidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "outcome_evidence_ref_required"):
            trial(outcome_evidence_ref="")

    def test_at_least_one_source_is_required(self):
        with self.assertRaisesRegex(ValueError, "at_least_one_source_contribution_required"):
            trial(source_contributions=())

    def test_duplicate_sources_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate_source_contribution"):
            trial(source_contributions=(source(), source()))

    def test_distribution_needs_authorized_terms_reference(self):
        with self.assertRaisesRegex(ValueError, "authorized_distribution_terms_reference_required"):
            trial(distribution_status="terms_authorized")

    def test_reconciliation_requires_verified_outcome(self):
        with self.assertRaisesRegex(ValueError, "distribution_cannot_be_reconciled_without_verified_outcome"):
            trial(outcome_status="pending", distribution_status="reconciled",
                  distribution_terms_ref="signed-terms-001")

    def test_reconciled_distribution_requires_terms_and_verified_outcome(self):
        result = trial(distribution_status="reconciled",
                       distribution_terms_ref="signed-terms-001")
        self.assertEqual(result.metrics()["distribution_status"], "reconciled")

    def test_zero_baseline_price_does_not_divide_by_zero(self):
        self.assertEqual(trial(baseline_total=Decimal("0"),
                               oneclick_total=Decimal("0")).price_improvement_percent,
                         Decimal("0"))

    def test_negative_time_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "oneclick_time_seconds_must_be_non_negative_integer"):
            trial(oneclick_time_seconds=-1)

    def test_invalid_currency_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "currency_required"):
            trial(currency="")


if __name__ == "__main__":
    unittest.main()
