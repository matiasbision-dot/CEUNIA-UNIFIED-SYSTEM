import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from core.proposal import create_proposal
from core.confirmation import record_confirmation
from core.confirmation_store import ConfirmationStore

class ConfirmationStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "memory" / "oneclick.sqlite3"
        self.store = ConfirmationStore(self.path)
        self.now = datetime(2026, 11, 14, 10, tzinfo=timezone.utc)
        self.proposal = create_proposal(
            merchant="Pizzeria Demo", region="Mar del Plata",
            product_id="pizza-mozz", product_name="Pizza mozzarella",
            quantity=2, modifiers=("extra queso",), fulfillment="pickup",
            destination_id=None, unit_price=Decimal("8500"), currency="ARS",
            catalog_source="sandbox_fixture", catalog_observed_at=self.now,
            created_at=self.now, max_age_seconds=600)
        self.record = record_confirmation(
            self.proposal, presented_proposal_id=self.proposal.proposal_id,
            decision="confirm", explicit_confirmation=True,
            decided_at=self.now + timedelta(minutes=1))

    def tearDown(self):
        self.temp.cleanup()

    def test_save_proposal_once_then_idempotent(self):
        self.assertTrue(self.store.save_proposal(self.proposal))
        self.assertFalse(self.store.save_proposal(self.proposal))

    def test_save_proposal_survives_reopen(self):
        self.store.save_proposal(self.proposal)
        reopened = ConfirmationStore(self.path)
        history = reopened.get_history(self.proposal.proposal_id)
        self.assertEqual(history["proposal"]["product_name"], "Pizza mozzarella")
        self.assertEqual(history["proposal"]["subtotal"], "17000")

    def test_confirmation_requires_saved_proposal(self):
        with self.assertRaisesRegex(ValueError, "proposal_must_be_saved_first"):
            self.store.record_decision(self.record)

    def test_confirmation_is_idempotent(self):
        self.store.save_proposal(self.proposal)
        self.assertTrue(self.store.record_decision(self.record))
        self.assertFalse(self.store.record_decision(self.record))

    def test_conflicting_second_decision_is_rejected(self):
        self.store.save_proposal(self.proposal)
        self.store.record_decision(self.record)
        declined = record_confirmation(
            self.proposal, presented_proposal_id=self.proposal.proposal_id,
            decision="decline", explicit_confirmation=True,
            decided_at=self.now + timedelta(minutes=2))
        with self.assertRaisesRegex(ValueError, "proposal_already_has_a_different_decision"):
            self.store.record_decision(declined)

    def test_outcome_requires_saved_proposal(self):
        with self.assertRaisesRegex(ValueError, "proposal_must_be_saved_first"):
            self.store.record_outcome(proposal_id=self.proposal.proposal_id,
                outcome="merchant_accepted", source="merchant_callback",
                observed_at=self.now, idempotency_key="evt-1")

    def test_outcome_is_idempotent(self):
        self.store.save_proposal(self.proposal)
        args = dict(proposal_id=self.proposal.proposal_id,
            outcome="merchant_accepted", source="verified_test_fixture",
            observed_at=self.now + timedelta(minutes=2),
            idempotency_key="event-001", external_reference="demo-order-1",
            details={"simulated": True})
        self.assertTrue(self.store.record_outcome(**args))
        self.assertFalse(self.store.record_outcome(**args))

    def test_reused_outcome_key_with_different_payload_rejected(self):
        self.store.save_proposal(self.proposal)
        args = dict(proposal_id=self.proposal.proposal_id,
            outcome="merchant_accepted", source="fixture",
            observed_at=self.now, idempotency_key="same-key")
        self.store.record_outcome(**args)
        with self.assertRaisesRegex(ValueError, "outcome_idempotency_conflict"):
            self.store.record_outcome(**{**args, "outcome":"merchant_rejected"})

    def test_history_contains_decision_and_outcome(self):
        self.store.save_proposal(self.proposal)
        self.store.record_decision(self.record)
        self.store.record_outcome(proposal_id=self.proposal.proposal_id,
            outcome="merchant_accepted", source="fixture",
            observed_at=self.now + timedelta(minutes=2),
            idempotency_key="event-002", details={"simulated": True})
        history = self.store.get_history(self.proposal.proposal_id)
        self.assertEqual(history["confirmation"]["status"], "CONFIRMED_FOR_NEXT_STEP")
        self.assertEqual(history["outcomes"][0]["outcome"], "merchant_accepted")

    def test_missing_proposal_history_rejected(self):
        with self.assertRaisesRegex(ValueError, "proposal_not_found"):
            self.store.get_history("missing")

    def test_outcome_timestamp_must_be_aware(self):
        self.store.save_proposal(self.proposal)
        with self.assertRaisesRegex(ValueError, "outcome_timestamp_must_be_timezone_aware"):
            self.store.record_outcome(proposal_id=self.proposal.proposal_id,
                outcome="unknown", source="fixture", observed_at=datetime(2026,11,14),
                idempotency_key="event-naive")

if __name__ == "__main__":
    unittest.main()
