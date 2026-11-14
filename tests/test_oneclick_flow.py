import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.catalog import CatalogItem, CatalogSnapshot
from core.oneclick_flow import prepare_order

class OneClickFlowTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 14, 12, tzinfo=timezone.utc)
        self.catalog = CatalogSnapshot("Pizzeria Demo", "Mar del Plata", "ARS",
            "verified_fixture", self.now - timedelta(seconds=20),
            (CatalogItem("pizza-mozz", "Pizza mozzarella", Decimal("12000"), True,
                         ("extra queso",)),))

    def run_flow(self, **overrides):
        args = dict(text="Quiero una pizza", catalog=self.catalog,
            product_id="pizza-mozz", fulfillment="delivery",
            destination_id="address-confirmed", now=self.now,
            max_catalog_age_seconds=60, merchant_available=True,
            modifiers=(), budget_limit=Decimal("15000"))
        args.update(overrides)
        return prepare_order(**args)

    def test_prepares_priced_order_without_execution(self):
        result = self.run_flow()
        self.assertEqual(result.status, "READY_FOR_REVIEW")
        self.assertEqual(result.prepared_order.total, Decimal("12000"))
        self.assertEqual(result.prepared_order.currency, "ARS")
        self.assertFalse(result.prepared_order.draft.confirmed)
        self.assertEqual(result.reason, "not_submitted_not_paid")

    def test_missing_fulfillment_asks_one_question(self):
        result = self.run_flow(fulfillment=None)
        self.assertEqual(result.status, "NEEDS_CLARIFICATION")
        self.assertEqual(result.questions, ("¿Con entrega o retiro?",))

    def test_delivery_requires_confirmed_destination(self):
        result = self.run_flow(destination_id=None)
        self.assertEqual(result.status, "NEEDS_CLARIFICATION")
        self.assertEqual(result.reason, "delivery_destination_required")

    def test_budget_limit_blocks_order(self):
        result = self.run_flow(budget_limit=Decimal("10000"))
        self.assertEqual(result.status, "OVER_BUDGET")

    def test_unavailable_merchant_blocks(self):
        result = self.run_flow(merchant_available=False)
        self.assertEqual(result.status, "UNAVAILABLE")

    def test_stale_catalog_blocks(self):
        result = self.run_flow(max_catalog_age_seconds=1)
        self.assertEqual(result.status, "CANNOT_PREPARE")
        self.assertEqual(result.reason, "catalog_snapshot_stale_or_future")

    def test_unverified_modifier_blocks(self):
        result = self.run_flow(modifiers=("ananá",))
        self.assertEqual(result.status, "CANNOT_PREPARE")

if __name__ == "__main__":
    unittest.main()
