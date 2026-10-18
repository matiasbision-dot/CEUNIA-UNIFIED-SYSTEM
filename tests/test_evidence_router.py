import unittest
from core.evidence_router import EvidenceRouter


class EvidenceRouterTests(unittest.TestCase):
    def test_fallback_without_enough_evidence(self):
        router = EvidenceRouter(models=("A", "B"), min_samples=2)
        self.assertEqual(router.select_model(task_type="forecast"), "A")
        self.assertIn("fallback", router.get_history()[-1]["reason"])

    def test_selects_lower_loss_after_min_samples(self):
        router = EvidenceRouter(models=("A", "B"), min_samples=3)
        for _ in range(3):
            router.record_result(model="A", task_type="forecast", metric="mae", value=0.2,
                                 dataset_id="heldout-v1", split="test")
            router.record_result(model="B", task_type="forecast", metric="mae", value=0.1,
                                 dataset_id="heldout-v1", split="test")
        self.assertEqual(router.select_model(task_type="forecast", metric="mae",
                                             dataset_id="heldout-v1", split="test"), "B")

    def test_selects_higher_metric_when_requested(self):
        router = EvidenceRouter(models=("A", "B"), min_samples=1)
        router.record_result(model="A", task_type="classify", metric="accuracy", value=0.8,
                             dataset_id="d1", split="validation")
        router.record_result(model="B", task_type="classify", metric="accuracy", value=0.9,
                             dataset_id="d1", split="validation")
        self.assertEqual(router.select_model(task_type="classify", metric="accuracy",
                                             dataset_id="d1", lower_is_better=False), "B")

    def test_does_not_mix_datasets(self):
        router = EvidenceRouter(models=("A", "B"), min_samples=1)
        router.record_result(model="B", task_type="forecast", metric="mae", value=0.01,
                             dataset_id="other", split="test")
        router.select_model(task_type="forecast", metric="mae", dataset_id="target", split="test")
        self.assertIn("fallback", router.get_history()[-1]["reason"])
        self.assertEqual(router.get_history()[-1]["sample_counts"]["B"], 0)

    def test_training_results_rejected(self):
        router = EvidenceRouter(models=("A",), min_samples=1)
        with self.assertRaises(ValueError):
            router.record_result(model="A", task_type="forecast", metric="mae", value=0.1,
                                 dataset_id="d1", split="train")

    def test_non_finite_metric_rejected(self):
        router = EvidenceRouter(models=("A",), min_samples=1)
        with self.assertRaises(ValueError):
            router.record_result(model="A", task_type="forecast", metric="mae", value=float("nan"),
                                 dataset_id="d1", split="test")

    def test_unknown_model_rejected(self):
        router = EvidenceRouter(models=("A",), min_samples=1)
        with self.assertRaises(ValueError):
            router.record_result(model="C", task_type="forecast", metric="mae", value=0.1,
                                 dataset_id="d1", split="test")


if __name__ == "__main__":
    unittest.main()
