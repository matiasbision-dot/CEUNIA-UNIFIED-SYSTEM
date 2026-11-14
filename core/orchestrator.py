"""Minimal CEUNIA Ω pipeline: validate quotes, rank, and stop before execution."""
from dataclasses import dataclass
from .adapters import ProviderAdapter
from .scoring import Offer, ScoredOffer, score_offers

@dataclass(frozen=True)
class Decision:
    status: str
    reason: str
    ranked: tuple[ScoredOffer, ...]
    execution_performed: bool = False

def compare_providers(intent: str, region: str, adapters: list[ProviderAdapter], *,
                      price_weight: float = 0.5, time_weight: float = 0.5) -> Decision:
    if not intent.strip() or not region.strip():
        return Decision("CONSULT", "intent_or_region_required", ())
    if not adapters:
        return Decision("ABSTAIN", "no_provider_adapters", ())
    quotes = []
    for adapter in adapters:
        capability = adapter.capability
        if not capability.supports_quote or capability.region != region:
            continue
        quote = adapter.quote(intent, region)
        if quote.provider != capability.provider:
            return Decision("ABSTAIN", "provider_identity_mismatch", ())
        if quote.environment != capability.environment:
            return Decision("ABSTAIN", "environment_mismatch", ())
        quotes.append(quote)
    available = [q for q in quotes if q.available]
    currencies = {q.currency for q in available}
    if len(currencies) > 1:
        return Decision("CONSULT", "currency_conversion_required", ())
    offers = [Offer(q.provider, q.price, q.eta_minutes, q.available, True) for q in quotes]
    ranked = score_offers(offers, price_weight=price_weight, time_weight=time_weight)
    if not ranked:
        return Decision("ABSTAIN", "no_feasible_quotes", ())
    return Decision("READY_FOR_USER_CONFIRMATION", "quote_comparison_only", tuple(ranked), False)
