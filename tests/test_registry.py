import unittest
from datetime import date
from core.registry import ProviderRecord, validate_registry

class ProviderRegistryTests(unittest.TestCase):
    def test_unverified_record_can_have_unknown_environment(self):
        record = ProviderRecord("Example", "food", "Argentina")
        self.assertEqual(record.status, "IDENTIFICADO")
        self.assertEqual(record.environment, "unknown")

    def test_verified_sandbox_requires_evidence_and_sandbox(self):
        with self.assertRaises(ValueError):
            ProviderRecord("Example", "food", "Argentina",
                           status="SANDBOX_VERIFICADO", environment="sandbox")
        record = ProviderRecord("Example", "food", "Argentina",
                                status="SANDBOX_VERIFICADO", environment="sandbox",
                                evidence=("tests/run-123",), checked_on=date(2026, 11, 14))
        self.assertEqual(record.evidence, ("tests/run-123",))

    def test_production_requires_production_environment(self):
        with self.assertRaises(ValueError):
            ProviderRecord("Example", "food", "Argentina",
                           status="PRODUCCION_VERIFICADA", environment="sandbox",
                           evidence=("receipt-1",))

    def test_rejects_duplicate_records(self):
        record = ProviderRecord("Example", "food", "Argentina")
        with self.assertRaises(ValueError):
            validate_registry((record, record))

    def test_registry_order_is_deterministic(self):
        b = ProviderRecord("Beta", "food", "Argentina")
        a = ProviderRecord("Alpha", "food", "Argentina")
        self.assertEqual([r.provider for r in validate_registry((b, a))],
                         ["Alpha", "Beta"])

if __name__ == "__main__":
    unittest.main()
