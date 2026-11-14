import os
import tempfile
import unittest
from core.execution import ExecutionReceipt
from core.ledger import SQLiteExecutionLedger

class SQLiteLedgerTests(unittest.TestCase):
    def test_reservation_and_receipt_survive_reopen(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "ledger.sqlite3")
            ledger = SQLiteExecutionLedger(path)
            self.assertTrue(ledger.reserve("key-1", "buy|Merchant|12|ARS|dest"))
            self.assertFalse(ledger.reserve("key-1", "different-payload"))
            ledger.record(ExecutionReceipt("Merchant", "key-1", "accepted", "receipt-1"))
            reopened = SQLiteExecutionLedger(path)
            item = reopened.get("key-1")
            self.assertEqual(item["status"], "RECORDED")
            self.assertEqual(item["receipt"]["external_reference"], "receipt-1")

    def test_cannot_record_without_reservation(self):
        with tempfile.TemporaryDirectory() as folder:
            ledger = SQLiteExecutionLedger(os.path.join(folder, "ledger.sqlite3"))
            with self.assertRaises(ValueError):
                ledger.record(ExecutionReceipt("Merchant", "missing", "accepted"))

if __name__ == "__main__":
    unittest.main()
