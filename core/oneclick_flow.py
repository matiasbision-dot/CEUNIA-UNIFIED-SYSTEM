"""Connect explicit ONECLICK intent to a fresh catalog without executing orders."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from .catalog import CatalogSnapshot
from .intent import resolve_intent
from .order_contract import OrderDraft, OrderLine, assess_order_readiness

@dataclass(frozen=True)
class PricedLine:
    line: OrderLine
    unit_price: Decimal
    line_total: Decimal

@dataclass(frozen=True)
class PreparedOrder:
    draft: OrderDraft
    priced_lines: tuple[PricedLine, ...]
    total: Decimal
    currency: str
    catalog_source: str
    catalog_observed_at: datetime

@dataclass(frozen=True)
class IntakeResult:
    status: str
    questions: tuple[str, ...] = ()
    prepared_order: PreparedOrder | None = None
    reason: str = ""

def prepare_order(text: str, *, catalog: CatalogSnapshot, product_id: str,
                  fulfillment: str | None, destination_id: str | None,
                  now: datetime, max_catalog_age_seconds: int,
                  merchant_available: bool,
                  modifiers: tuple[str, ...] = (),
                  budget_limit: Decimal | None = None) -> IntakeResult:
    """Prepare a priced, reviewable order; never submit or charge."""
    intent = resolve_intent(text)
    questions = list(intent.questions)
    if intent.product is None:
        return IntakeResult("NEEDS_CLARIFICATION", tuple(questions), reason="product_not_unambiguous")
    if intent.quantity is None:
        return IntakeResult("NEEDS_CLARIFICATION", tuple(questions), reason="quantity_missing")
    if fulfillment not in ("delivery", "pickup"):
        return IntakeResult("NEEDS_CLARIFICATION", ("¿Con entrega o retiro?",),
                            reason="explicit_fulfillment_required")
    if fulfillment == "delivery" and not (destination_id and destination_id.strip()):
        return IntakeResult("NEEDS_CLARIFICATION", ("¿A qué dirección confirmada lo enviamos?",),
                            reason="delivery_destination_required")
    if catalog.region.casefold().strip() == "" or not merchant_available:
        return IntakeResult("UNAVAILABLE", reason="merchant_unavailable_or_region_missing")
    try:
        line = catalog.build_order_line(product_id, quantity=intent.quantity,
            now=now, max_age_seconds=max_catalog_age_seconds, modifiers=modifiers)
    except ValueError as exc:
        return IntakeResult("CANNOT_PREPARE", reason=str(exc))
    priced = PricedLine(line, catalog.items[[x.product_id for x in catalog.items].index(product_id)].price,
                        catalog.items[[x.product_id for x in catalog.items].index(product_id)].price * intent.quantity)
    if budget_limit is not None:
        if not budget_limit.is_finite() or budget_limit < 0:
            return IntakeResult("CANNOT_PREPARE", reason="invalid_budget_limit")
        if priced.line_total > budget_limit:
            return IntakeResult("OVER_BUDGET", reason="budget_limit_exceeded")
    draft = OrderDraft(
        merchant_id=catalog.provider, region=catalog.region,
        fulfillment=fulfillment, lines=(line,), destination_id=destination_id,
        budget_limit=float(budget_limit) if budget_limit is not None else None,
        currency=catalog.currency, preference_source="user_explicit", confirmed=False)
    readiness = assess_order_readiness(draft, catalog_verified=True,
                                       merchant_available=merchant_available)
    if not readiness.ready_for_quote:
        return IntakeResult("NOT_READY", reason=",".join(readiness.missing))
    prepared = PreparedOrder(draft, (priced,), priced.line_total, catalog.currency,
                             catalog.source, catalog.observed_at)
    return IntakeResult("READY_FOR_REVIEW", prepared_order=prepared,
                        reason="not_submitted_not_paid")
