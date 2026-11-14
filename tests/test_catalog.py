import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.catalog import CatalogItem, CatalogSnapshot

class CatalogSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 14, 12, tzinfo=timezone.utc)
        self.snapshot = CatalogSnapshot(
            provider="Merchant", region="Mar del Plata", currency="ARS",
            source="merchant_catalog_api",
            observed_at=self.now - timedelta(minutes=2),
            items=(CatalogItem("pizza-mozz", "Pizza mozzarella", Decimal("12500"),
                               True, ("extra queso", "sin aceitunas")),
                   CatalogItem("pizza-jamon", "Pizza jamón", Decimal("14500"), False))
        )

    def test_fresh_snapshot_builds_only_catalogued_order_line(self):
        line = self.snapshot.build_order_line("pizza-mozz", quantity=1,
            now=self.now, max_age_seconds=300, modifiers=("extra queso",))
        self.assertEqual(line.product_id, "pizza-mozz")
        self.assertEqual(line.modifiers, ("extra queso",))

    def test_stale_snapshot_cannot_be_used(self):
        with self.assertRaisesRegex(ValueError, "catalog_snapshot_stale_or_future"):
            self.snapshot.select_item("pizza-mozz", now=self.now,
                                      max_age_seconds=30)

    def test_unavailable_item_cannot_be_selected(self):
        with self.assertRaisesRegex(ValueError, "product_unavailable"):
            self.snapshot.select_item("pizza-jamon", now=self.now,
                                      max_age_seconds=300)

    def test_unknown_modifier_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "modifier_not_in_verified_catalog"):
            self.snapshot.build_order_line("pizza-mozz", quantity=1,
                now=self.now, max_age_seconds=300, modifiers=("ananá",))

    def test_future_snapshot_is_rejected(self):
        future = CatalogSnapshot("Merchant", "Mar del Plata", "ARS", "api",
            self.now + timedelta(minutes=1), (CatalogItem("sku", "Producto", 100, True),))
        self.assertFalse(future.is_fresh(now=self.now, max_age_seconds=300))

    def test_catalog_requires_timezone_aware_timestamp(self):
        with self.assertRaises(ValueError):
            CatalogSnapshot("Merchant", "Mar del Plata", "ARS", "api",
                datetime(2026, 11, 14), ())

    def test_invalid_price_is_rejected(self):
        with self.assertRaises(ValueError):
            CatalogItem("sku", "Producto", Decimal("NaN"), True)

if __name__ == "__main__":
    unittest.main()
