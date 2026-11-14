import unittest
from core.adapters import Capability
from core.consent import ActionRequest
from core.registry import ProviderRecord
from core.execution import ExecutionReceipt, execute_authorized

class FakeLedger:
    def __init__(self):
        self.keys = {}
        self.receipts = []
    def reserve(self, key, fingerprint):
        if key in self.keys:
            return False
        self.keys[key] = fingerprint
        return True
    def record(self, receipt):
        self.receipts.append(receipt)

class FakeProductionAdapter:
    def __init__(self):
        self.capability = Capability("Merchant", "food", "Argentina", True, True, "production")
        self.calls = 0
    def execute(self, request):
        self.calls += 1
        return ExecutionReceipt(request.provider, request.idempotency_key, "accepted", "ext-123")

def record():
    return ProviderRecord("Merchant", "food", "Argentina",
        status="PRODUCCION_VERIFICADA", environment="production",
        evidence=("independent-production-test-001",))

def request(key="order-001"):
    return ActionRequest("place_order", "Merchant", 12000, "ARS", "address-confirmed", key)

class ExecutionGatewayTests(unittest.TestCase):
    def setUp(self):
        self.adapter = FakeProductionAdapter()
        self.ledger = FakeLedger()
    def test_no_execution_without_explicit_confirmation(self):
        result = execute_authorized(request(), confirmed=False, provider_record=record(),
            adapter=self.adapter, ledger=self.ledger, budget_limit=15000)
        self.assertEqual(result.reason, "explicit_confirmation_required")
        self.assertEqual(self.adapter.calls, 0)
    def test_no_execution_for_unverified_provider(self):
        unverified = ProviderRecord("Merchant", "food", "Argentina")
        result = execute_authorized(request(), confirmed=True, provider_record=unverified,
            adapter=self.adapter, ledger=self.ledger)
        self.assertEqual(result.reason, "provider_not_production_verified")
        self.assertEqual(self.adapter.calls, 0)
    def test_success_requires_receipt_and_records_it(self):
        result = execute_authorized(request(), confirmed=True, provider_record=record(),
            adapter=self.adapter, ledger=self.ledger, budget_limit=15000)
        self.assertEqual(result.status, "EXECUTED")
        self.assertTrue(result.execution_performed)
        self.assertEqual(len(self.ledger.receipts), 1)
    def test_idempotency_blocks_second_execution(self):
        args = dict(confirmed=True, provider_record=record(), adapter=self.adapter,
                    ledger=self.ledger, budget_limit=15000)
        execute_authorized(request(), **args)
        result = execute_authorized(request(), **args)
        self.assertEqual(result.reason, "duplicate_or_conflicting_idempotency_key")
        self.assertEqual(self.adapter.calls, 1)
    def test_budget_limit_blocks_execution(self):
        result = execute_authorized(request(), confirmed=True, provider_record=record(),
            adapter=self.adapter, ledger=self.ledger, budget_limit=100)
        self.assertEqual(result.reason, "budget_limit_exceeded")
        self.assertEqual(self.adapter.calls, 0)

    def test_incomplete_receipt_requires_reconciliation(self):
        class BadReceiptAdapter(FakeProductionAdapter):
            def execute(self, request):
                self.calls += 1
                return ExecutionReceipt(request.provider, request.idempotency_key, "accepted", None)
        adapter = BadReceiptAdapter()
        result = execute_authorized(request(), confirmed=True, provider_record=record(),
            adapter=adapter, ledger=self.ledger, budget_limit=15000)
        self.assertEqual(result.reason, "incomplete_provider_receipt")
        self.assertFalse(result.execution_performed)


    def test_rejected_provider_receipt_is_not_reported_as_execution(self):
        class RejectingAdapter(FakeProductionAdapter):
            def execute(self, request):
                self.calls += 1
                return ExecutionReceipt(request.provider, request.idempotency_key,
                                        "rejected", "ext-reject")
        adapter = RejectingAdapter()
        result = execute_authorized(request(), confirmed=True, provider_record=record(),
            adapter=adapter, ledger=self.ledger, budget_limit=15000)
        self.assertEqual(result.status, "REJECTED")
        self.assertFalse(result.execution_performed)
        self.assertEqual(len(self.ledger.receipts), 1)

    def test_unknown_provider_receipt_status_requires_reconciliation(self):
        class PendingAdapter(FakeProductionAdapter):
            def execute(self, request):
                self.calls += 1
                return ExecutionReceipt(request.provider, request.idempotency_key,
                                        "processing", "ext-pending")
        adapter = PendingAdapter()
        result = execute_authorized(request(), confirmed=True, provider_record=record(),
            adapter=adapter, ledger=self.ledger, budget_limit=15000)
        self.assertEqual(result.status, "RECONCILIATION_REQUIRED")
        self.assertFalse(result.execution_performed)

    def test_unsupported_action_is_blocked(self):
        req = ActionRequest("refund", "Merchant", 12000, "ARS",
                            "address-confirmed", "order-refund")
        result = execute_authorized(req, confirmed=True, provider_record=record(),
            adapter=self.adapter, ledger=self.ledger, budget_limit=15000)
        self.assertEqual(result.reason, "unsupported_action")
        self.assertEqual(self.adapter.calls, 0)

    def test_adapter_must_be_production_order_capable(self):
        self.adapter.capability = Capability("Merchant", "food", "Argentina", True, False, "production")
        result = execute_authorized(request(), confirmed=True, provider_record=record(),
            adapter=self.adapter, ledger=self.ledger)
        self.assertEqual(result.reason, "adapter_not_production_order_capable")
        self.assertEqual(self.adapter.calls, 0)

if __name__ == "__main__":
    unittest.main()
