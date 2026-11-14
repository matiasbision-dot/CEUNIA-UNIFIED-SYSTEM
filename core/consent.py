"""Explicit consent gate for externally consequential actions."""
from dataclasses import dataclass
from math import isfinite

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
    if not request.currency.strip():
        return False, "missing_currency"
    if request.amount is not None and (not isfinite(request.amount) or request.amount < 0):
        return False, "invalid_amount"
    if budget_limit is not None and (not isfinite(budget_limit) or budget_limit < 0):
        return False, "invalid_budget_limit"
    if budget_limit is not None and request.amount is not None and request.amount > budget_limit:
        return False, "budget_limit_exceeded"
    if not request.idempotency_key or not request.idempotency_key.strip():
        return False, "missing_idempotency_key"
    if not confirmed:
        return False, "explicit_confirmation_required"
    return True, "authorized"
