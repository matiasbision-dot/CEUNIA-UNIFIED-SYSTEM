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


    def test_quantity_is_bound_to_product_not_unrelated_numbers(self):
        result = resolve_intent("Quiero pizza para 2 personas")
        self.assertEqual(result.product, "pizza")
        self.assertEqual(result.quantity, 1)

    def test_explicit_quantity_before_product(self):
        result = resolve_intent("Quiero dos pizzas con delivery")
        self.assertEqual(result.quantity, 2)
        self.assertEqual(result.fulfillment, "delivery")

    def test_quantity_after_product_marker(self):
        result = resolve_intent("Pizza x3 para retirar")
        self.assertEqual(result.quantity, 3)
        self.assertEqual(result.fulfillment, "pickup")

    def test_multiple_products_require_clarification(self):
        result = resolve_intent("Quiero pizza y sushi")
        self.assertIsNone(result.product)
        self.assertEqual(set(result.product_candidates), {"pizza", "sushi"})
        self.assertIn("product", result.missing)

    def test_negated_delivery_is_not_misread_as_delivery(self):
        result = resolve_intent("Quiero pizza sin delivery")
        self.assertIsNone(result.fulfillment)
        self.assertIn("fulfillment", result.missing)

    def test_conflicting_modalities_require_clarification(self):
        result = resolve_intent("Quiero pizza con delivery y retiro")
        self.assertIsNone(result.fulfillment)

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            resolve_intent("  ")

if __name__ == "__main__":
    unittest.main()
