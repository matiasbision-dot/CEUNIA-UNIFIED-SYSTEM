"""Minimal CEUNIA Ω pipeline: quote, rank, and stop before execution."""
from dataclasses import dataclass
from .adapters import ProviderAdapter
from .scoring import Offer, score_offers

@dataclass(frozen=True)
class Decision:
    status: str
    reason: str
    ranked: tuple
    execution_performed: bool = False

def compare_providers(intent: str, region: str, adapters: list[ProviderAdapter], *,
                      price_weight: float = 0.5, time_weight: float = 0.5) -> Decision:
    quotes = [a.quote(intent, region) for a in adapters]
    if not quotes:
        return Decision("ABSTAIN", "no_provider_adapters", ())
    currencies = {q.currency for q in quotes if q.available}
    if len(currencies) > 1:
        return Decision("CONSULT", "currency_conversion_required", ())
    offers = [Offer(q.provider, q.price, q.eta_minutes, q.available, True) for q in quotes]
    ranked = score_offers(offers, price_weight=price_weight, time_weight=time_weight)
    if not ranked:
        return Decision("ABSTAIN", "no_feasible_quotes", ())
    # External execution is intentionally absent; confirmation and a live authorized
    # provider adapter are separate requirements.
    return Decision("READY_FOR_USER_CONFIRMATION", "quote_comparison_only", tuple(ranked), False)
