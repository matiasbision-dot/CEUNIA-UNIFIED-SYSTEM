"""Deterministic, dependency-free scoring for comparable provider offers."""
from dataclasses import dataclass
from typing import Iterable, Optional

@dataclass(frozen=True)
class Offer:
    provider: str
    price: float
    minutes: float
    available: bool = True
    authorized: bool = True

@dataclass(frozen=True)
class ScoredOffer:
    offer: Offer
    price_norm: float
    time_norm: float
    score: float

def score_offers(offers: Iterable[Offer], *, price_weight: float = 0.5,
                 time_weight: float = 0.5, max_price: Optional[float] = None,
                 max_minutes: Optional[float] = None) -> list[ScoredOffer]:
    """Rank feasible offers; lower score is better. Excludes unavailable/unauthorized."""
    if price_weight < 0 or time_weight < 0 or price_weight + time_weight <= 0:
        raise ValueError("Weights must be non-negative and sum to a positive value")
    total = price_weight + time_weight
    pw, tw = price_weight / total, time_weight / total
    candidates = [o for o in offers if o.available and o.authorized]
    for o in candidates:
        if o.price < 0 or o.minutes < 0:
            raise ValueError("Price and minutes must be non-negative")
    if max_price is not None:
        candidates = [o for o in candidates if o.price <= max_price]
    if max_minutes is not None:
        candidates = [o for o in candidates if o.minutes <= max_minutes]
    if not candidates:
        return []
    pmin, pmax = min(o.price for o in candidates), max(o.price for o in candidates)
    tmin, tmax = min(o.minutes for o in candidates), max(o.minutes for o in candidates)
    scored = []
    for o in candidates:
        pn = (o.price - pmin) / (pmax - pmin) if pmax != pmin else 0.0
        tn = (o.minutes - tmin) / (tmax - tmin) if tmax != tmin else 0.0
        scored.append(ScoredOffer(o, pn, tn, pw * pn + tw * tn))
    return sorted(scored, key=lambda s: (s.score, s.offer.price, s.offer.minutes, s.offer.provider))
