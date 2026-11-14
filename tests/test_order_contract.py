import unittest
from core.order_contract import OrderDraft, OrderLine, assess_order_readiness

class OrderContractTests(unittest.TestCase):
    def valid(self, **changes):
        data = dict(merchant_id="merchant-1", region="Mar del Plata",
                    fulfillment="delivery",
                    lines=(OrderLine("sku-1", "Pizza mozzarella", 1),),
                    destination_id="address-confirmed",
                    preference_source="user_explicit")
        data.update(changes)
        return OrderDraft(**data)

    def test_valid_draft_is_not_automatically_ready_without_live_checks(self):
        draft = self.valid()
        readiness = assess_order_readiness(draft, catalog_verified=False,
                                           merchant_available=False)
        self.assertFalse(readiness.ready_for_quote)
        self.assertEqual(readiness.missing,
                         ("verified_catalog", "merchant_availability"))

    def test_verified_catalog_and_availability_enable_quote_stage_only(self):
        result = assess_order_readiness(self.valid(), catalog_verified=True,
                                        merchant_available=True)
        self.assertTrue(result.ready_for_quote)

    def test_delivery_requires_selected_destination(self):
        with self.assertRaises(ValueError):
            self.valid(destination_id=None)

    def test_pickup_does_not_require_delivery_destination(self):
        draft = self.valid(fulfillment="pickup", destination_id=None)
        self.assertEqual(draft.fulfillment, "pickup")

    def test_rejects_non_integer_or_zero_quantity(self):
        for value in (0, -1, 1.5, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    OrderLine("sku", "Pizza", value)

    def test_rejects_unconfirmed_preference_origin(self):
        with self.assertRaises(ValueError):
            self.valid(preference_source="model_guess")

    def test_rejects_negative_budget(self):
        with self.assertRaises(ValueError):
            self.valid(budget_limit=-1)

if __name__ == "__main__":
    unittest.main()
