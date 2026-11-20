import unittest
from ceunia.metacode.evolution import evaluate_experiment, build_cer_bundle


class MetaCodeEvolutionTests(unittest.TestCase):
    def base_report(self, **overrides):
        report = {
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
            "source_hashes": [],
        }
        report.update(overrides)
        return report

    def test_nasa_reported_metrics_are_preserved(self):
        result = evaluate_experiment(self.base_report())
        self.assertEqual(result.status, "REPORTED_IMPROVEMENT_PENDING_REPRODUCTION")
        self.assertAlmostEqual(result.metrics["model_mae_improvement_pct"], 7.6477728, places=5)
        self.assertAlmostEqual(result.metrics["walkforward_vs_baseline_improvement_pct"], 8.248, places=2)
        self.assertEqual(result.metrics["test_n"], 493)

    def test_reproduced_boolean_and_arbitrary_hash_do_not_upgrade_evidence(self):
        result = evaluate_experiment(self.base_report(
            reproduced=True, source_hashes=["abc"]
        ))
        self.assertEqual(result.evidence_grade, "REPORTED_RESULT_NOT_INDEPENDENTLY_REPRODUCED")
        self.assertEqual(result.point_albedrio, "REPRODUCE_ON_EXISTING_ARTIFACTS")

    def test_complete_reproduction_metadata_still_requires_audit(self):
        result = evaluate_experiment(self.base_report(reproduction={
            "protocol_id": "protocol-v1",
            "independent_reviewer": "reviewer-01",
            "run_id": "run-2026-001",
            "artifacts": [{"path": "results/report.json", "sha256": "a" * 64}],
        }))
        self.assertEqual(result.evidence_grade, "REPRODUCTION_METADATA_COMPLETE_PENDING_AUDIT")
        self.assertEqual(result.point_albedrio, "INDEPENDENT_REPRODUCTION_AUDIT")

    def test_no_improvement_never_recommends_pilot(self):
        result = evaluate_experiment(self.base_report(model_mae=1.30))
        self.assertEqual(result.status, "NO_IMPROVEMENT")
        self.assertEqual(result.point_albedrio, "HOLD_AND_REVIEW")
        self.assertIn("do not advance", result.next_action)

    def test_record_hash_is_deterministic_and_timestamp_independent(self):
        report = self.base_report()
        first = evaluate_experiment(report)
        second = evaluate_experiment(report)
        self.assertEqual(first.record_hash, second.record_hash)

    def test_invalid_hash_and_boolean_sample_size_are_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_experiment(self.base_report(source_hashes=["abc"]))
        with self.assertRaises(ValueError):
            evaluate_experiment(self.base_report(test_n=True))

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
