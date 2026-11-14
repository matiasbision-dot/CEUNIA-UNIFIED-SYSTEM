import unittest
from core.intent import resolve_intent

class IntentResolutionTests(unittest.TestCase):
    def test_simple_pizza_does_not_invent_variant_or_merchant(self):
        result = resolve_intent("Quiero una pizza")
        self.assertEqual(result.product, "pizza")
        self.assertEqual(result.quantity, 1)
        self.assertIsNone(result.fulfillment)
        self.assertIn("fulfillment", result.missing)
        self.assertFalse(result.intent_slots_complete)

    def test_explicit_quantity_and_delivery(self):
        result = resolve_intent("Quiero 2 pizzas con delivery")
        self.assertEqual(result.product, "pizza")
        self.assertEqual(result.quantity, 2)
        self.assertEqual(result.fulfillment, "delivery")
        self.assertTrue(result.intent_slots_complete)

    def test_pickup_and_accent_normalization(self):
        result = resolve_intent("Quiero café para retirar")
        self.assertEqual(result.product, "cafe")
        self.assertEqual(result.fulfillment, "pickup")

    def test_conflicting_fulfillment_requires_clarification(self):
        result = resolve_intent("Pizza con delivery y paso a buscar")
        self.assertIsNone(result.fulfillment)
        self.assertIn("fulfillment", result.missing)

    def test_unknown_product_is_not_guessed(self):
        result = resolve_intent("Quiero algo rico")
        self.assertIsNone(result.product)
        self.assertIn("product", result.missing)

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            resolve_intent("  ")

if __name__ == "__main__":
    unittest.main()
