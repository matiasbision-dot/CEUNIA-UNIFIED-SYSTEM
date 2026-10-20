import unittest
from ceunia.metacode.evolution import evaluate_experiment, build_cer_bundle


class MetaCodeEvolutionTests(unittest.TestCase):
    def test_nasa_reported_metrics_are_preserved(self):
        result = evaluate_experiment({
            "experiment_id": "NASA-POWER-2026-10",
            "domain": "environmental_prediction",
            "baseline_mae": 1.291156186612576,
            "model_mae": 1.1924114948962365,
            "walkforward_mae": 1.1846364064690789,
            "test_n": 493,
            "configurations_passed": 99,
            "configurations_total": 99,
            "source": "NASA POWER (reported by operator)",
            "period": ["2020-01-01", "2026-10-14"],
            "source_hashes": ["abc"],
            "reproduced": False,
        })
        self.assertEqual(result.status, "REPORTED_IMPROVEMENT_PENDING_REPRODUCTION")
        self.assertAlmostEqual(result.metrics["model_mae_improvement_pct"], 7.6477728, places=5)
        self.assertAlmostEqual(result.metrics["walkforward_vs_baseline_improvement_pct"], 8.248, places=2)
        self.assertEqual(result.metrics["test_n"], 493)

    def test_missing_finance_result_is_not_fabricated(self):
        with self.assertRaises(ValueError):
            evaluate_experiment({
                "experiment_id": "FINANCE-GOLD-2026",
                "domain": "finance",
                "baseline_mae": None,
                "model_mae": None,
            })

    def test_bundle_has_hash_and_bounded_policy(self):
        bundle = build_cer_bundle([{
            "experiment_id": "NASA-1", "domain": "climate",
            "baseline_mae": 1.0, "model_mae": 0.9,
            "source": "test", "period": "2020-2026",
        }])
        self.assertEqual(bundle["experiment_count"], 1)
        self.assertEqual(len(bundle["bundle_sha256"]), 64)
        self.assertEqual(bundle["evolution_policy"]["finance_execution"], "research_only_no_trading")


if __name__ == "__main__":
    unittest.main()
