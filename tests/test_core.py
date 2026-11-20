import tempfile
import unittest
from pathlib import Path
from ceunia_omega.core import CEUNIAEngine

class CEUNIAEngineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.engine = CEUNIAEngine(Path(self.tmp.name) / "events.sqlite3")
        self.engine.register_executor("default", lambda task: "processed: " + task)

    def tearDown(self):
        self.tmp.cleanup()

    def test_run_and_hash_chain(self):
        result = self.engine.run("hello")
        self.assertEqual(result["validation"]["status"], "PASS")
        self.assertEqual(result["output"], "processed: hello")
        verified = self.engine.verify_provenance()
        self.assertTrue(verified["valid"])
        self.assertEqual(verified["events_checked"], 1)

    def test_approval_gate_does_not_execute(self):
        called = []
        self.engine.register_executor("default", lambda task: called.append(task) or "done")
        result = self.engine.run("delete resource", requires_approval=True)
        self.assertEqual(result["validation"]["status"], "BLOCKED")
        self.assertIsNone(result["output"])
        self.assertEqual(called, [])

    def test_empty_output_fails(self):
        self.engine.register_executor("default", lambda task: " ")
        self.assertEqual(self.engine.run("hello")["validation"]["status"], "FAIL")

    def test_unknown_route_falls_back(self):
        self.engine.router.set_route("analysis", "not-registered")
        result = self.engine.run("hello", "analysis")
        self.assertEqual(result["route"]["executor_name"], "default")
        self.assertEqual(result["route"]["reason"], "fallback_to_default")

if __name__ == "__main__":
    unittest.main()
