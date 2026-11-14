"""Explicit consent gate for externally consequential actions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ActionRequest:
    action: str
    provider: str
    amount: float | None = None
    currency: str = "ARS"
    destination: str | None = None
    idempotency_key: str | None = None

def authorize_action(request: ActionRequest, *, confirmed: bool,
                     budget_limit: float | None = None) -> tuple[bool, str]:
    if not request.action.strip() or not request.provider.strip():
        return False, "missing_action_or_provider"
    if request.amount is not None and request.amount < 0:
        return False, "invalid_amount"
    if budget_limit is not None and request.amount is not None and request.amount > budget_limit:
        return False, "budget_limit_exceeded"
    if not request.idempotency_key:
        return False, "missing_idempotency_key"
    if not confirmed:
        return False, "explicit_confirmation_required"
    return True, "authorized"
