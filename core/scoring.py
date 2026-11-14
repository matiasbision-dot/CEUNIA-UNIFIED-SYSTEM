"""Deterministic, validated scoring for comparable provider offers."""
from dataclasses import dataclass
from math import isfinite
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

def _finite_non_negative(value: float, field: str) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{field} must be finite and non-negative")

def score_offers(offers: Iterable[Offer], *, price_weight: float = 0.5,
                 time_weight: float = 0.5, max_price: Optional[float] = None,
                 max_minutes: Optional[float] = None) -> list[ScoredOffer]:
    """Rank feasible offers; lower score is better. Hard filters run before ranking."""
    _finite_non_negative(price_weight, "price_weight")
    _finite_non_negative(time_weight, "time_weight")
    if price_weight + time_weight <= 0:
        raise ValueError("At least one weight must be positive")
    if max_price is not None:
        _finite_non_negative(max_price, "max_price")
    if max_minutes is not None:
        _finite_non_negative(max_minutes, "max_minutes")

    total = price_weight + time_weight
    pw, tw = price_weight / total, time_weight / total
    candidates = []
    for offer in offers:
        if not offer.provider.strip():
            raise ValueError("Provider name cannot be empty")
        _finite_non_negative(offer.price, "price")
        _finite_non_negative(offer.minutes, "minutes")
        if offer.available and offer.authorized:
            if max_price is not None and offer.price > max_price:
                continue
            if max_minutes is not None and offer.minutes > max_minutes:
                continue
            candidates.append(offer)
    if not candidates:
        return []

    pmin, pmax = min(o.price for o in candidates), max(o.price for o in candidates)
    tmin, tmax = min(o.minutes for o in candidates), max(o.minutes for o in candidates)
    scored = []
    for offer in candidates:
        pn = (offer.price - pmin) / (pmax - pmin) if pmax != pmin else 0.0
        tn = (offer.minutes - tmin) / (tmax - tmin) if tmax != tmin else 0.0
        scored.append(ScoredOffer(offer, pn, tn, pw * pn + tw * tn))
    return sorted(scored, key=lambda s: (s.score, s.offer.price, s.offer.minutes, s.offer.provider.casefold()))
