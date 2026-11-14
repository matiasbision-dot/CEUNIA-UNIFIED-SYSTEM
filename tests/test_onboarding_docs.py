from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = {
    "MERCHANT-AUTHORIZATION-v0.1.md": [
        "NO FIRMADA",
        "finalidad",
        "revocación",
        "autorización de ejecución",
    ],
    "MERCHANT-CATALOG-SPEC-v0.1.md": [
        "price_amount",
        "currency",
        "valid_until",
        "source_id",
        "UNKNOWN",
    ],
    "ONECLICK-MERCHANT-ADAPTER-v0.1.md": [
        "READ_ONLY",
        "PROPOSAL",
        "EXECUTION",
        "idempotencia",
        "timeout",
    ],
    "ECONOMIC-PILOT-PROTOCOL-v0.1.md": [
        "Tiempo ahorrado",
        "Errores evitados",
        "Mejora de precio",
        "Contribución de fuente",
        "Distribución de valor",
        "NO MEDIDO",
    ],
    "TRACEABILITY-AND-EVIDENCE-v0.1.md": [
        "SHA-256",
        "SQLite",
        "get_history",
        "FIXTURE",
        "no prueba autoría",
    ],
}


class MerchantOnboardingDocumentationTests(unittest.TestCase):
    def test_all_five_documents_exist_and_are_nonempty(self):
        for filename in REQUIRED_DOCS:
            with self.subTest(filename=filename):
                path = ROOT / filename
                self.assertTrue(path.is_file(), f"Missing document: {filename}")
                self.assertGreater(path.stat().st_size, 500, filename)

    def test_each_document_contains_its_safety_and_scope_controls(self):
        for filename, required_markers in REQUIRED_DOCS.items():
            content = (ROOT / filename).read_text(encoding="utf-8")
            normalized = content.casefold()
            with self.subTest(filename=filename):
                for marker in required_markers:
                    self.assertIn(marker.casefold(), normalized, f"{filename}: missing {marker}")

    def test_traceability_event_name_is_well_formed(self):
        content = (ROOT / "TRACEABILITY-AND-EVIDENCE-v0.1.md").read_text(encoding="utf-8")
        self.assertIn("ECONOMIC_MEASUREMENT_RECORDED", content)
        self.assertNotIn("ECONOMIC_MEASUREMENT_RECORDED)", content)


if __name__ == "__main__":
    unittest.main()
