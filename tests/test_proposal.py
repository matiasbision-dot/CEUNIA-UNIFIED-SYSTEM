import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.proposal import create_proposal

class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.observed = datetime(2026, 11, 14, 10, tzinfo=timezone.utc)
        self.now = self.observed + timedelta(minutes=2)

    def make(self, **changes):
        args = dict(merchant="Pizzeria Demo", region="Mar del Plata",
            product_id="pizza-mozz", product_name="Pizza mozzarella",
            quantity=2, modifiers=("extra queso",), fulfillment="delivery",
            destination_id="address-confirmed", unit_price=Decimal("8500"),
            currency="ARS", catalog_source="merchant_catalog_api",
            catalog_observed_at=self.observed, created_at=self.now,
            max_age_seconds=300)
        args.update(changes)
        return create_proposal(**args)

    def test_proposal_has_auditable_price_and_expiry(self):
        proposal = self.make()
        self.assertEqual(proposal.subtotal, Decimal("17000"))
        self.assertEqual(proposal.currency, "ARS")
        self.assertEqual(proposal.availability, "available")
        self.assertEqual(proposal.price_kind, "catalog_subtotal")
        self.assertEqual(proposal.valid_until, self.observed + timedelta(seconds=300))

    def test_proposal_is_not_submission_or_payment(self):
        proposal = self.make()
        self.assertTrue(proposal.requires_user_confirmation)
        self.assertFalse(proposal.submitted)
        self.assertFalse(proposal.paid)
        self.assertFalse(proposal.final_total_confirmed)

    def test_same_evidence_yields_same_proposal_id(self):
        self.assertEqual(self.make().proposal_id, self.make().proposal_id)

    def test_changed_quantity_changes_proposal_id(self):
        self.assertNotEqual(self.make().proposal_id,
                            self.make(quantity=1).proposal_id)

    def test_stale_catalog_rejected(self):
        with self.assertRaisesRegex(ValueError, "catalog_snapshot_stale_or_future"):
            self.make(max_age_seconds=30)

    def test_pickup_cannot_carry_delivery_destination(self):
        with self.assertRaisesRegex(ValueError, "pickup_must_not_include_delivery_destination"):
            self.make(fulfillment="pickup")

    def test_delivery_requires_destination(self):
        with self.assertRaisesRegex(ValueError, "proposal_destination_required"):
            self.make(destination_id=None)

    def test_non_decimal_or_invalid_price_rejected(self):
        with self.assertRaisesRegex(ValueError, "proposal_price_invalid"):
            self.make(unit_price=Decimal("NaN"))

if __name__ == "__main__":
    unittest.main()
