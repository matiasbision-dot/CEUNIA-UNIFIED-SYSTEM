"""Conservative Spanish intent extraction for ONECLICK.

Only explicit and unambiguous signals are extracted. This module never chooses
a merchant, product variant, price, address or preference on the user's behalf.
"""
from dataclasses import dataclass
import re
import unicodedata

PRODUCTS = {
    "pizza": ("pizza", "pizzas"),
    "hamburguesa": ("hamburguesa", "hamburguesas", "burger", "burgers"),
    "sushi": ("sushi",),
    "empanadas": ("empanada", "empanadas"),
    "cafe": ("cafe", "cafes"),
    "agua": ("agua",),
}
DELIVERY_PATTERNS = (r"\bdelivery\b", r"\benvio\b", r"\ba domicilio\b")
PICKUP_PATTERNS = (r"\bretiro\b", r"\bretirar\b", r"\bpaso a buscar\b", r"\btake away\b")
NEGATION = r"\b(?:no|sin|nunca)\b"

@dataclass(frozen=True)
class IntentResolution:
    raw_text: str
    normalized_text: str
    product: str | None
    quantity: int | None
    fulfillment: str | None
    missing: tuple[str, ...]
    questions: tuple[str, ...]
    product_candidates: tuple[str, ...] = ()

    @property
    def intent_slots_complete(self) -> bool:
        return self.product is not None and self.quantity is not None and self.fulfillment is not None

def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in value if not unicodedata.combining(ch))

def _matches(patterns: tuple[str, ...], text: str) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)

def resolve_intent(text: str) -> IntentResolution:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("intent text is required")
    normalized = _normalize(text)

    found = []
    for canonical, variants in PRODUCTS.items():
        if any(re.search(r"\b" + re.escape(_normalize(term)) + r"\b", normalized)
               for term in variants):
            found.append(canonical)
    candidates = tuple(found)
    product = candidates[0] if len(candidates) == 1 else None

    quantity = None
    number_words = {"una": 1, "uno": 1, "un": 1, "dos": 2, "tres": 3,
                    "cuatro": 4, "cinco": 5, "seis": 6}
    number_pattern = r"(?:[1-9][0-9]?|" + "|".join(number_words) + r")"
    if product:
        variants = "|".join(re.escape(_normalize(v)) for v in PRODUCTS[product])
        # Accept quantity only when it is attached to the product phrase.
        before = re.search(r"\b(" + number_pattern + r")\s+(?:" + variants + r")\b", normalized)
        after = re.search(r"\b(?:" + variants + r")\s*(?:x|por)\s*(" + number_pattern + r")\b", normalized)
        match = before or after
        if match:
            token = match.group(1)
            quantity = int(token) if token.isdigit() else number_words[token]
        elif product in {"pizza", "hamburguesa", "cafe", "agua"}:
            quantity = 1

    delivery = _matches(DELIVERY_PATTERNS, normalized)
    pickup = _matches(PICKUP_PATTERNS, normalized)
    # A negated modality is not permission to infer the opposite modality.
    delivery_negated = bool(re.search(NEGATION + r"\s+(?:quiero\s+)?(?:el\s+)?(?:delivery|envio|a domicilio)\b", normalized))
    pickup_negated = bool(re.search(NEGATION + r"\s+(?:quiero\s+)?(?:retirar|retiro|paso a buscar|take away)\b", normalized))
    if delivery_negated:
        delivery = False
    if pickup_negated:
        pickup = False
    fulfillment = "delivery" if delivery and not pickup else (
        "pickup" if pickup and not delivery else None
    )

    missing = []
    questions = []
    if product is None:
        missing.append("product")
        questions.append("¿Qué producto querés pedir?" if len(candidates) != 0 else "¿Qué querés pedir?")
    if quantity is None:
        missing.append("quantity")
        questions.append("¿Cuántas unidades?")
    if fulfillment is None:
        missing.append("fulfillment")
        questions.append("¿Con entrega o retiro?")
    return IntentResolution(text, normalized, product, quantity, fulfillment,
                            tuple(missing), tuple(questions), candidates)
