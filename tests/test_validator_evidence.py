import unittest
from core.validator_evidence import CEUNIAEvidenceValidator, ValidationPolicy


class EvidenceValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = CEUNIAEvidenceValidator()
        self.good = {
            "objective": "Evaluate a proposed action",
            "evidence": ["source:A", "measurement:B"],
            "risk_score": 0.10,
            "uncertainty_score": 0.20,
            "evidence_quality": 0.90,
        }

    def test_approves_complete_low_risk_record(self):
        self.assertEqual(self.validator.evaluate(self.good)["status"], "APPROVE")

    def test_missing_record_fails_closed(self):
        result = self.validator.evaluate(None)
        self.assertEqual(result["status"], "HOLD")
        self.assertIn("missing_objective", result["reasons"])

    def test_high_risk_is_held(self):
        record = {**self.good, "risk_score": 0.90}
        result = self.validator.evaluate(record)
        self.assertEqual(result["status"], "HOLD")
        self.assertIn("risk_above_policy", result["reasons"])

    def test_missing_evidence_is_held(self):
        record = {**self.good, "evidence": []}
        self.assertEqual(self.validator.evaluate(record)["status"], "HOLD")

    def test_invalid_range_is_held(self):
        record = {**self.good, "risk_score": 2}
        self.assertEqual(self.validator.evaluate(record)["status"], "HOLD")

    def test_policy_is_configurable(self):
        validator = CEUNIAEvidenceValidator(ValidationPolicy(max_risk=0.15))
        record = {**self.good, "risk_score": 0.20}
        self.assertEqual(validator.evaluate(record)["status"], "HOLD")

    def test_record_hash_is_present(self):
        result = self.validator.evaluate(self.good)
        self.assertEqual(len(result["record_sha256"]), 64)

    def test_history_is_recorded(self):
        self.validator.evaluate(self.good)
        self.assertEqual(len(self.validator.get_history()), 1)


if __name__ == "__main__":
    unittest.main()
