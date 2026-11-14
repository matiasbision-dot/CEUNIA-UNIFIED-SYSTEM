"""Immutable, traceable ONECLICK proposal for human review.

A proposal is not an order submission, final checkout total, or payment.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import json

@dataclass(frozen=True)
class OrderProposal:
    proposal_id: str
    merchant: str
    region: str
    product_id: str
    product_name: str
    quantity: int
    modifiers: tuple[str, ...]
    fulfillment: str
    destination_id: str | None
    unit_price: Decimal
    subtotal: Decimal
    currency: str
    availability: str
    catalog_source: str
    catalog_observed_at: datetime
    created_at: datetime
    valid_until: datetime
    price_kind: str = "catalog_subtotal"
    final_total_confirmed: bool = False
    requires_user_confirmation: bool = True
    submitted: bool = False
    paid: bool = False

def create_proposal(*, merchant: str, region: str, product_id: str,
                    product_name: str, quantity: int, modifiers: tuple[str, ...],
                    fulfillment: str, destination_id: str | None,
                    unit_price: Decimal, currency: str, catalog_source: str,
                    catalog_observed_at: datetime, created_at: datetime,
                    max_age_seconds: int) -> OrderProposal:
    if not all(isinstance(x, str) and x.strip() for x in
               (merchant, region, product_id, product_name, currency, catalog_source)):
        raise ValueError("proposal_identity_and_provenance_required")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("proposal_quantity_invalid")
    if fulfillment not in ("delivery", "pickup"):
        raise ValueError("proposal_fulfillment_invalid")
    if fulfillment == "delivery" and not (destination_id and destination_id.strip()):
        raise ValueError("proposal_destination_required")
    if fulfillment == "pickup" and destination_id is not None:
        raise ValueError("pickup_must_not_include_delivery_destination")
    if catalog_observed_at.tzinfo is None or catalog_observed_at.utcoffset() is None:
        raise ValueError("catalog_timestamp_must_be_timezone_aware")
    if created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("proposal_timestamp_must_be_timezone_aware")
    if max_age_seconds < 0:
        raise ValueError("max_age_seconds_invalid")
    if not isinstance(unit_price, Decimal) or not unit_price.is_finite() or unit_price < 0:
        raise ValueError("proposal_price_invalid")
    valid_until = catalog_observed_at + timedelta(seconds=max_age_seconds)
    if created_at < catalog_observed_at or created_at > valid_until:
        raise ValueError("catalog_snapshot_stale_or_future")
    if any(not isinstance(m, str) or not m.strip() for m in modifiers):
        raise ValueError("proposal_modifier_invalid")
    subtotal = unit_price * quantity
    payload = {
        "merchant": merchant, "region": region, "product_id": product_id,
        "product_name": product_name, "quantity": quantity,
        "modifiers": list(modifiers), "fulfillment": fulfillment,
        "destination_id": destination_id, "unit_price": str(unit_price),
        "subtotal": str(subtotal), "currency": currency,
        "catalog_source": catalog_source,
        "catalog_observed_at": catalog_observed_at.isoformat(),
        "created_at": created_at.isoformat(), "valid_until": valid_until.isoformat(),
    }
    proposal_id = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return OrderProposal(
        proposal_id, merchant, region, product_id, product_name, quantity,
        tuple(modifiers), fulfillment, destination_id, unit_price, subtotal,
        currency, "available", catalog_source, catalog_observed_at,
        created_at, valid_until,
    )
