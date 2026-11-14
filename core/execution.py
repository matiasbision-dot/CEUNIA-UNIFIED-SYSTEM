"""Fail-closed execution gateway. No production adapter or ledger is bundled."""
from dataclasses import dataclass
from typing import Protocol
from .adapters import Capability
from .consent import ActionRequest, authorize_action
from .registry import ProviderRecord

@dataclass(frozen=True)
class ExecutionReceipt:
    provider: str
    idempotency_key: str
    status: str
    external_reference: str | None = None

class ExecutionAdapter(Protocol):
    capability: Capability
    def execute(self, request: ActionRequest) -> ExecutionReceipt: ...

class ExecutionLedger(Protocol):
    """Implementations MUST atomically reserve keys and persist outcomes durably."""
    def reserve(self, key: str, fingerprint: str) -> bool: ...
    def record(self, receipt: ExecutionReceipt) -> None: ...

@dataclass(frozen=True)
class ExecutionDecision:
    status: str
    reason: str
    receipt: ExecutionReceipt | None = None
    execution_performed: bool = False

def execute_authorized(request: ActionRequest, *, confirmed: bool,
                       provider_record: ProviderRecord,
                       adapter: ExecutionAdapter,
                       ledger: ExecutionLedger,
                       budget_limit: float | None = None) -> ExecutionDecision:
    """Execute only with explicit confirmation, production evidence and an atomic ledger."""
    capability = adapter.capability
    if provider_record.provider.casefold() != request.provider.casefold():
        return ExecutionDecision("ABSTAIN", "provider_record_mismatch")
    if provider_record.status != "PRODUCCION_VERIFICADA" or provider_record.environment != "production":
        return ExecutionDecision("ABSTAIN", "provider_not_production_verified")
    if capability.provider.casefold() != request.provider.casefold():
        return ExecutionDecision("ABSTAIN", "adapter_provider_mismatch")
    if capability.environment != "production" or not capability.supports_order:
        return ExecutionDecision("ABSTAIN", "adapter_not_production_order_capable")
    if request.amount is None or request.destination is None or not request.destination.strip():
        return ExecutionDecision("CONSULT", "amount_and_destination_required")
    ok, reason = authorize_action(request, confirmed=confirmed, budget_limit=budget_limit)
    if not ok:
        return ExecutionDecision("CONSULT", reason)
    fingerprint = "|".join((request.action, request.provider, str(request.amount),
                            request.currency, request.destination))
    if not ledger.reserve(request.idempotency_key, fingerprint):
        return ExecutionDecision("ABSTAIN", "duplicate_or_conflicting_idempotency_key")
    try:
        receipt = adapter.execute(request)
    except Exception:
        return ExecutionDecision("RECONCILIATION_REQUIRED", "provider_execution_outcome_unknown")
    if receipt.provider.casefold() != request.provider.casefold():
        return ExecutionDecision("RECONCILIATION_REQUIRED", "receipt_provider_mismatch")
    if receipt.idempotency_key != request.idempotency_key:
        return ExecutionDecision("RECONCILIATION_REQUIRED", "receipt_idempotency_mismatch")
    ledger.record(receipt)
    return ExecutionDecision("EXECUTED", "provider_receipt_recorded", receipt, True)
