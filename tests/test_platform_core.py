import unittest
from core.scoring import Offer, score_offers
from core.consent import ActionRequest, authorize_action
from core.adapters import Capability, Quote, DemoAdapter
from core.orchestrator import compare_providers

class ScoringTests(unittest.TestCase):
    def test_balanced_score_prefers_best_tradeoff(self):
        result = score_offers([Offer("A", 100, 30), Offer("B", 120, 10), Offer("C", 200, 60)])
        self.assertEqual(result[0].offer.provider, "B")
    def test_filters_unavailable_and_unauthorized(self):
        self.assertEqual(score_offers([Offer("A", 1, 1, False), Offer("B", 2, 2, True, False)]), [])
    def test_constant_dimensions(self):
        result = score_offers([Offer("A", 10, 5), Offer("B", 10, 8)])
        self.assertEqual(result[0].price_norm, 0)
        self.assertEqual(result[0].score, 0)
    def test_hard_caps(self):
        result = score_offers([Offer("A", 10, 5), Offer("B", 20, 5)], max_price=15)
        self.assertEqual([x.offer.provider for x in result], ["A"])
    def test_invalid_weights_and_values(self):
        with self.assertRaises(ValueError): score_offers([Offer("A", 1, 1)], price_weight=0, time_weight=0)
        with self.assertRaises(ValueError): score_offers([Offer("A", -1, 1)])

class ConsentTests(unittest.TestCase):
    def request(self):
        return ActionRequest("place_order", "demo", 100, "ARS", "user-confirmed", "once-123")
    def test_confirmation_required(self):
        ok, reason = authorize_action(self.request(), confirmed=False)
        self.assertFalse(ok)
        self.assertEqual(reason, "explicit_confirmation_required")
    def test_budget_limit(self):
        ok, reason = authorize_action(self.request(), confirmed=True, budget_limit=50)
        self.assertFalse(ok)
        self.assertEqual(reason, "budget_limit_exceeded")
    def test_authorized_after_confirmation(self):
        ok, reason = authorize_action(self.request(), confirmed=True, budget_limit=150)
        self.assertTrue(ok)
        self.assertEqual(reason, "authorized")

class OrchestrationTests(unittest.TestCase):
    def adapter(self, name, price, eta):
        cap = Capability(name, "food", "Mar del Plata", True, False, "sandbox")
        quote = Quote(name, price, "ARS", eta, True, "fixture", "sandbox")
        return DemoAdapter(cap, quote)
    def test_compares_but_never_executes(self):
        result = compare_providers("pizza", "Mar del Plata",
            [self.adapter("A", 8500, 25), self.adapter("B", 9200, 18)])
        self.assertEqual(result.status, "READY_FOR_USER_CONFIRMATION")
        self.assertFalse(result.execution_performed)
        self.assertEqual(len(result.ranked), 2)
    def test_no_adapter_abstains(self):
        self.assertEqual(compare_providers("pizza", "Mar del Plata", []).status, "ABSTAIN")

if __name__ == "__main__":
    unittest.main()
