"""Validated consumer order draft; this module never contacts a merchant or charges."""
from dataclasses import dataclass, field
from math import isfinite
from typing import Literal

Fulfillment = Literal["delivery", "pickup"]

@dataclass(frozen=True)
class OrderLine:
    product_id: str
    display_name: str
    quantity: int = 1
    modifiers: tuple[str, ...] = ()
    note: str = ""

    def __post_init__(self):
        if not self.product_id.strip() or not self.display_name.strip():
            raise ValueError("product_id and display_name are required")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int) or self.quantity < 1:
            raise ValueError("quantity must be a positive integer")
        if any(not item.strip() for item in self.modifiers):
            raise ValueError("modifiers cannot contain empty values")

@dataclass(frozen=True)
class OrderDraft:
    merchant_id: str
    region: str
    fulfillment: Fulfillment
    lines: tuple[OrderLine, ...]
    destination_id: str | None = None
    budget_limit: float | None = None
    currency: str = "ARS"
    preference_source: str = "user_explicit"
    confirmed: bool = False

    def __post_init__(self):
        if not self.merchant_id.strip() or not self.region.strip():
            raise ValueError("merchant_id and region are required")
        if self.fulfillment not in ("delivery", "pickup"):
            raise ValueError("fulfillment must be delivery or pickup")
        if not self.lines:
            raise ValueError("at least one order line is required")
        if self.fulfillment == "delivery" and not (self.destination_id and self.destination_id.strip()):
            raise ValueError("delivery requires a selected destination")
        if self.budget_limit is not None and (
            not isfinite(self.budget_limit) or self.budget_limit < 0
        ):
            raise ValueError("budget_limit must be finite and non-negative")
        if not self.currency.strip():
            raise ValueError("currency is required")
        if self.preference_source not in ("user_explicit", "user_confirmed_memory"):
            raise ValueError("preferences must be explicit or previously confirmed")

@dataclass(frozen=True)
class OrderReadiness:
    ready_for_quote: bool
    missing: tuple[str, ...] = field(default_factory=tuple)

def assess_order_readiness(draft: OrderDraft, *, catalog_verified: bool,
                           merchant_available: bool) -> OrderReadiness:
    missing = []
    if not catalog_verified:
        missing.append("verified_catalog")
    if not merchant_available:
        missing.append("merchant_availability")
    return OrderReadiness(not missing, tuple(missing))
