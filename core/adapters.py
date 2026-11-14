"""Provider adapter contracts and a sandbox-only demonstration adapter."""
from dataclasses import dataclass
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
        self.capability = capability
        self._quote = quote

    def quote(self, intent: str, region: str) -> Quote:
        if region != self.capability.region:
            return Quote(self.capability.provider, 0, self._quote.currency, 0, False,
                         "region_not_supported", "sandbox")
        return self._quote
