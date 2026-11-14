import math
import unittest
from core.scoring import Offer, score_offers
from core.adapters import Capability, Quote, DemoAdapter
from core.orchestrator import compare_providers
from core.consent import ActionRequest, authorize_action

class HardeningTests(unittest.TestCase):
    def test_rejects_non_finite_inputs(self):
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    score_offers([Offer("A", value, 5)])
    def test_rejects_empty_provider(self):
        with self.assertRaises(ValueError):
            score_offers([Offer(" ", 10, 5)])
    def test_rejects_invalid_limits(self):
        with self.assertRaises(ValueError):
            score_offers([Offer("A", 10, 5)], max_price=math.inf)
    def test_demo_adapter_rejects_provider_mismatch(self):
        cap = Capability("A", "food", "Mar del Plata", True)
        quote = Quote("B", 100, "ARS", 10, True, "fixture", "sandbox")
        with self.assertRaises(ValueError):
            DemoAdapter(cap, quote)
    def test_demo_adapter_rejects_non_sandbox(self):
        cap = Capability("A", "food", "Mar del Plata", True, environment="live")
        quote = Quote("A", 100, "ARS", 10, True, "fixture", "live")
        with self.assertRaises(ValueError):
            DemoAdapter(cap, quote)
    def test_currency_mismatch_requires_consultation(self):
        a = DemoAdapter(Capability("A", "food", "Mar del Plata", True),
                        Quote("A", 100, "ARS", 10, True, "fixture", "sandbox"))
        b = DemoAdapter(Capability("B", "food", "Mar del Plata", True),
                        Quote("B", 100, "USD", 10, True, "fixture", "sandbox"))
        decision = compare_providers("pizza", "Mar del Plata", [a, b])
        self.assertEqual(decision.status, "CONSULT")
        self.assertEqual(decision.reason, "currency_conversion_required")
    def test_empty_intent_does_not_call_provider(self):
        decision = compare_providers("", "Mar del Plata", [])
        self.assertEqual(decision.reason, "intent_or_region_required")
    def test_consent_rejects_non_finite_amount(self):
        req = ActionRequest("buy", "provider", math.nan, "ARS", "dest", "key")
        self.assertEqual(authorize_action(req, confirmed=True)[1], "invalid_amount")
    def test_consent_rejects_invalid_budget(self):
        req = ActionRequest("buy", "provider", 10, "ARS", "dest", "key")
        self.assertEqual(authorize_action(req, confirmed=True, budget_limit=math.inf)[1],
                         "invalid_budget_limit")

if __name__ == "__main__":
    unittest.main()
