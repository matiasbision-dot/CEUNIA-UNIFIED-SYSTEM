import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.proposal import create_proposal
from core.confirmation import record_confirmation

class ConfirmationTests(unittest.TestCase):
    def setUp(self):
        self.created = datetime(2026, 11, 14, 10, tzinfo=timezone.utc)
        self.decided = self.created + timedelta(minutes=1)
        self.proposal = create_proposal(
            merchant="Pizzeria Demo", region="Mar del Plata",
            product_id="pizza-mozz", product_name="Pizza mozzarella",
            quantity=1, modifiers=(), fulfillment="pickup",
            destination_id=None, unit_price=Decimal("8500"), currency="ARS",
            catalog_source="sandbox_fixture",
            catalog_observed_at=self.created, created_at=self.created,
            max_age_seconds=300)

    def decide(self, **changes):
        args = dict(proposal=self.proposal,
            presented_proposal_id=self.proposal.proposal_id,
            decision="confirm", explicit_confirmation=True,
            decided_at=self.decided)
        args.update(changes)
        return record_confirmation(**args)

    def test_confirm_records_decision_but_never_executes(self):
        record = self.decide()
        self.assertEqual(record.status, "CONFIRMED_FOR_NEXT_STEP")
        self.assertEqual(record.proposal_id, self.proposal.proposal_id)
        self.assertFalse(record.execution_authorized)
        self.assertFalse(record.order_submitted)
        self.assertFalse(record.payment_taken)

    def test_decline_records_no_execution(self):
        record = self.decide(decision="decline")
        self.assertEqual(record.status, "DECLINED")
        self.assertFalse(record.execution_authorized)

    def test_exact_proposal_id_is_required(self):
        with self.assertRaisesRegex(ValueError, "presented_proposal_mismatch"):
            self.decide(presented_proposal_id="different")

    def test_confirmation_must_be_explicit(self):
        with self.assertRaisesRegex(ValueError, "explicit_user_decision_required"):
            self.decide(explicit_confirmation=False)

    def test_expired_proposal_requires_refresh(self):
        with self.assertRaisesRegex(ValueError, "proposal_expired_refresh_required"):
            self.decide(decided_at=self.proposal.valid_until + timedelta(seconds=1))

    def test_naive_timestamp_rejected(self):
        with self.assertRaisesRegex(ValueError, "decision_timestamp_must_be_timezone_aware"):
            self.decide(decided_at=datetime(2026, 11, 14, 10, 1))

    def test_decision_before_proposal_rejected(self):
        with self.assertRaisesRegex(ValueError, "decision_precedes_proposal"):
            self.decide(decided_at=self.created - timedelta(seconds=1))

    def test_unknown_decision_rejected(self):
        with self.assertRaisesRegex(ValueError, "decision_must_be_confirm_or_decline"):
            self.decide(decision="maybe")

if __name__ == "__main__":
    unittest.main()
