import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.live_data import LiveDataRecord, assess_live_data, ResolutionValue

NOW = datetime(2026, 11, 14, 12, tzinfo=timezone.utc)

class LiveDataContractTests(unittest.TestCase):
    def record(self, **changes):
        values = dict(source="merchant_catalog_api", source_type="merchant_catalog",
            observed_at=NOW-timedelta(seconds=10), expires_at=NOW+timedelta(minutes=5),
            purpose="prepare_quote", permission_granted=True,
            permission_scope="prepare_quote", quality_score=Decimal("0.95"),
            value="8500.00", unit="ARS", context_ref="merchant:pizzeria-demo")
        values.update(changes)
        return LiveDataRecord(**values)

    def test_valid_observation_is_usable_for_declared_purpose(self):
        result = assess_live_data(self.record(), now=NOW, requested_purpose="prepare_quote")
        self.assertTrue(result.usable)
        self.assertEqual(result.reason, "live_data_usable_for_declared_purpose")

    def test_missing_permission_fails_closed(self):
        result = assess_live_data(self.record(permission_granted=False), now=NOW, requested_purpose="prepare_quote")
        self.assertFalse(result.usable)
        self.assertEqual(result.reason, "permission_not_granted")

    def test_purpose_cannot_be_reused_outside_scope(self):
        result = assess_live_data(self.record(), now=NOW, requested_purpose="targeted_ads")
        self.assertFalse(result.usable)
        self.assertEqual(result.reason, "purpose_or_permission_scope_mismatch")

    def test_expired_observation_is_rejected(self):
        result = assess_live_data(self.record(expires_at=NOW), now=NOW, requested_purpose="prepare_quote")
        self.assertFalse(result.usable)
        self.assertEqual(result.reason, "observation_not_current")

    def test_future_observation_is_rejected(self):
        result = assess_live_data(self.record(observed_at=NOW+timedelta(seconds=1), expires_at=NOW+timedelta(minutes=5)),
            now=NOW, requested_purpose="prepare_quote")
        self.assertFalse(result.usable)

    def test_low_quality_observation_is_rejected(self):
        result = assess_live_data(self.record(quality_score=Decimal("0.2")), now=NOW,
            requested_purpose="prepare_quote", minimum_quality=Decimal("0.5"))
        self.assertFalse(result.usable)
        self.assertEqual(result.reason, "quality_below_threshold")

    def test_record_id_is_deterministic(self):
        self.assertEqual(self.record().record_id, self.record().record_id)

    def test_invalid_quality_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "quality_score_must_be_between_zero_and_one"):
            self.record(quality_score=Decimal("1.1"))

    def test_naive_clock_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "now_must_be_timezone_aware"):
            assess_live_data(self.record(), now=datetime(2026, 11, 14, 12), requested_purpose="prepare_quote")

    def test_resolution_value_requires_measured_evidence(self):
        evidence = ResolutionValue("resolution-1", (self.record().record_id,),
            "merchant_accepted", Decimal("8500"), "ARS", NOW, "merchant_order_receipt")
        self.assertTrue(evidence.is_measured_evidence)

    def test_resolution_value_rejects_missing_data_lineage(self):
        with self.assertRaisesRegex(ValueError, "data_record_ids_required"):
            ResolutionValue("resolution-1", (), "accepted", Decimal("1"), "ARS", NOW, "receipt")

if __name__ == "__main__":
    unittest.main()