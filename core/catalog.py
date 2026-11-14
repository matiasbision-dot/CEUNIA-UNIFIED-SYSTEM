"""Evidence-aware catalog snapshots for ONECLICK.

A catalog item is usable only when it comes from a named source, is available,
and belongs to a fresh snapshot. This module does not fetch live data.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from .order_contract import OrderLine

@dataclass(frozen=True)
class CatalogItem:
    product_id: str
    name: str
    price: Decimal
    available: bool
    modifiers: tuple[str, ...] = ()

    def __post_init__(self):
        try:
            price = Decimal(str(self.price))
        except (InvalidOperation, ValueError):
            raise ValueError("price must be a valid decimal")
        if not self.product_id.strip() or not self.name.strip():
            raise ValueError("product_id and name are required")
        if not price.is_finite() or price < 0:
            raise ValueError("price must be finite and non-negative")
        object.__setattr__(self, "price", price)
        if any(not m.strip() for m in self.modifiers):
            raise ValueError("modifiers cannot be empty")

@dataclass(frozen=True)
class CatalogSnapshot:
    provider: str
    region: str
    currency: str
    source: str
    observed_at: datetime
    items: tuple[CatalogItem, ...]

    def __post_init__(self):
        for value in (self.provider, self.region, self.currency, self.source):
            if not value.strip():
                raise ValueError("provider, region, currency and source are required")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        ids = [item.product_id for item in self.items]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate product ids in catalog snapshot")

    def is_fresh(self, *, now: datetime, max_age_seconds: int) -> bool:
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("now must be timezone-aware")
        if max_age_seconds < 0:
            raise ValueError("max_age_seconds must be non-negative")
        age = (now - self.observed_at).total_seconds()
        return 0 <= age <= max_age_seconds

    def select_item(self, product_id: str, *, now: datetime,
                    max_age_seconds: int) -> CatalogItem:
        if not self.is_fresh(now=now, max_age_seconds=max_age_seconds):
            raise ValueError("catalog_snapshot_stale_or_future")
        item = next((x for x in self.items if x.product_id == product_id), None)
        if item is None:
            raise ValueError("product_not_in_verified_catalog")
        if not item.available:
            raise ValueError("product_unavailable")
        return item

    def build_order_line(self, product_id: str, *, quantity: int, now: datetime,
                         max_age_seconds: int,
                         modifiers: tuple[str, ...] = ()) -> OrderLine:
        item = self.select_item(product_id, now=now, max_age_seconds=max_age_seconds)
        unknown = set(modifiers) - set(item.modifiers)
        if unknown:
            raise ValueError("modifier_not_in_verified_catalog")
        return OrderLine(item.product_id, item.name, quantity, modifiers)
