"""Provider adapter contracts and a strictly sandbox-only demo adapter."""
from dataclasses import dataclass
from math import isfinite
from typing import Protocol

@dataclass(frozen=True)
class Capability:
    provider: str
    category: str
    region: str
    supports_quote: bool
    supports_order: bool = False
    environment: str = "sandbox"

@dataclass(frozen=True)
class Quote:
    provider: str
    price: float
    currency: str
    eta_minutes: float
    available: bool
    source: str
    environment: str

class ProviderAdapter(Protocol):
    capability: Capability
    def quote(self, intent: str, region: str) -> Quote: ...

class DemoAdapter:
    """Returns fixture data only; never contacts a company or places an order."""
    def __init__(self, capability: Capability, quote: Quote):
        if capability.environment != "sandbox" or quote.environment != "sandbox":
            raise ValueError("DemoAdapter accepts sandbox data only")
        if not capability.provider.strip() or quote.provider != capability.provider:
            raise ValueError("Quote provider must match capability provider")
        if not capability.supports_quote:
            raise ValueError("Capability does not support quotes")
        if not quote.currency.strip() or not quote.source.strip():
            raise ValueError("Quote currency and source are required")
        if not isfinite(quote.price) or quote.price < 0:
            raise ValueError("Quote price must be finite and non-negative")
        if not isfinite(quote.eta_minutes) or quote.eta_minutes < 0:
            raise ValueError("Quote ETA must be finite and non-negative")
        self.capability = capability
        self._quote = quote

    def quote(self, intent: str, region: str) -> Quote:
        if not intent.strip():
            raise ValueError("Intent cannot be empty")
        if region != self.capability.region:
            return Quote(self.capability.provider, 0, self._quote.currency, 0, False,
                         "region_not_supported", "sandbox")
        return self._quote
