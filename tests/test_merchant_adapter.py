import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.proposal import create_proposal
from core.confirmation import record_confirmation
from core.merchant_adapter import (MerchantCapability, MerchantSubmission,
    validate_submission_boundary, submit_confirmed_order)

class FakeMerchantAdapter:
    def __init__(self, capability):
        self.capability = capability
        self.calls = 0
    def submit_order(self, proposal, *, confirmation, idempotency_key):
        self.calls += 1
        return MerchantSubmission(proposal.merchant, "demo-123", "accepted",
            "fake_adapter_test", NOW, idempotency_key)

NOW = datetime(2026, 11, 14, 12, tzinfo=timezone.utc)

class MerchantAdapterBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.proposal = create_proposal(merchant="Pizzeria Demo", region="Mar del Plata",
            product_id="pizza", product_name="Pizza mozzarella", quantity=1,
            modifiers=(), fulfillment="pickup", destination_id=None,
            unit_price=Decimal("8500"), currency="ARS", catalog_source="fixture",
            catalog_observed_at=NOW - timedelta(seconds=5), created_at=NOW - timedelta(seconds=1),
            max_age_seconds=120)
        self.confirmation = record_confirmation(self.proposal,
            presented_proposal_id=self.proposal.proposal_id, decision="confirm",
            explicit_confirmation=True, decided_at=NOW)
        self.capability = MerchantCapability("Pizzeria Demo", "Mar del Plata",
            "production", True, True, True)

    def check(self, **changes):
        values = dict(proposal=self.proposal, confirmation=self.confirmation,
            capability=self.capability, now=NOW, explicit_external_authorization=True)
        values.update(changes)
        return validate_submission_boundary(**values)

    def test_valid_boundary_passes_without_calling_merchant(self):
        self.assertEqual(self.check(), (True, "submission_preconditions_met"))

    def test_external_authorization_is_required(self):
        ok, reason = self.check(explicit_external_authorization=False)
        self.assertFalse(ok)
        self.assertEqual(reason, "external_execution_authorization_required")

    def test_confirmation_must_match_proposal(self):
        wrong = record_confirmation(self.proposal, presented_proposal_id=self.proposal.proposal_id,
            decision="decline", explicit_confirmation=True, decided_at=NOW)
        ok, reason = self.check(confirmation=wrong)
        self.assertFalse(ok)
        self.assertEqual(reason, "explicit_confirmation_required")

    def test_mismatched_proposal_confirmation_rejected(self):
        other = create_proposal(merchant="Pizzeria Demo", region="Mar del Plata",
            product_id="pizza-2", product_name="Pizza especial", quantity=1,
            modifiers=(), fulfillment="pickup", destination_id=None,
            unit_price=Decimal("9000"), currency="ARS", catalog_source="fixture",
            catalog_observed_at=NOW - timedelta(seconds=5), created_at=NOW - timedelta(seconds=1),
            max_age_seconds=120)
        ok, reason = self.check(proposal=other)
        self.assertFalse(ok)
        self.assertEqual(reason, "confirmation_proposal_mismatch")

    def test_sandbox_adapter_cannot_submit(self):
        cap = MerchantCapability("Pizzeria Demo", "Mar del Plata", "sandbox", True, True, True)
        ok, reason = self.check(capability=cap)
        self.assertFalse(ok)
        self.assertEqual(reason, "production_adapter_required")

    def test_adapter_must_support_orders(self):
        cap = MerchantCapability("Pizzeria Demo", "Mar del Plata", "production", True, False, True)
        ok, reason = self.check(capability=cap)
        self.assertFalse(ok)
        self.assertEqual(reason, "merchant_order_submission_not_supported")

    def test_remote_idempotency_is_mandatory(self):
        cap = MerchantCapability("Pizzeria Demo", "Mar del Plata", "production", True, True, False)
        ok, reason = self.check(capability=cap)
        self.assertFalse(ok)
        self.assertEqual(reason, "merchant_idempotency_required")

    def test_merchant_identity_must_match(self):
        cap = MerchantCapability("Other Shop", "Mar del Plata", "production", True, True, True)
        ok, reason = self.check(capability=cap)
        self.assertFalse(ok)
        self.assertEqual(reason, "merchant_identity_mismatch")

    def test_expired_proposal_rejected(self):
        ok, reason = self.check(now=self.proposal.valid_until + timedelta(seconds=1))
        self.assertFalse(ok)
        self.assertEqual(reason, "proposal_expired_or_not_yet_valid")

    def test_invalid_timestamp_rejected(self):
        ok, reason = self.check(now=datetime(2026, 11, 14, 12))
        self.assertFalse(ok)
        self.assertEqual(reason, "current_timestamp_must_be_timezone_aware")

    def test_missing_idempotency_key_does_not_call_adapter(self):
        adapter = FakeMerchantAdapter(self.capability)
        with self.assertRaisesRegex(ValueError, "merchant_idempotency_key_required"):
            submit_confirmed_order(adapter, self.proposal, self.confirmation,
                now=NOW, idempotency_key="", explicit_external_authorization=True)
        self.assertEqual(adapter.calls, 0)

    def test_valid_fake_submission_is_validated(self):
        adapter = FakeMerchantAdapter(self.capability)
        result = submit_confirmed_order(adapter, self.proposal, self.confirmation,
            now=NOW, idempotency_key="proposal-" + self.proposal.proposal_id,
            explicit_external_authorization=True)
        self.assertEqual(result.status, "accepted")
        self.assertEqual(adapter.calls, 1)

    def test_default_does_not_authorize_external_execution(self):
        adapter = FakeMerchantAdapter(self.capability)
        with self.assertRaises(PermissionError):
            submit_confirmed_order(adapter, self.proposal, self.confirmation,
                now=NOW, idempotency_key="key")
        self.assertEqual(adapter.calls, 0)

if __name__ == "__main__":
    unittest.main()