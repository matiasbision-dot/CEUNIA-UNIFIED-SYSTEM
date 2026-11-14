"""Conservative Spanish intent extraction for ONECLICK.

Extracts only explicit signals. It never chooses a merchant, product variant,
price, address or preference on the user's behalf.
"""
from dataclasses import dataclass
import re
import unicodedata

PRODUCTS = {
    "pizza": ("pizza",),
    "hamburguesa": ("hamburguesa", "hamburguesas", "burger", "hamburguesa"),
    "sushi": ("sushi",),
    "empanadas": ("empanada", "empanadas"),
    "cafe": ("cafe", "café"),
    "agua": ("agua",),
}
DELIVERY_TERMS = ("delivery", "envio", "envío", "a domicilio")
PICKUP_TERMS = ("retiro", "retirar", "paso a buscar", "take away")

@dataclass(frozen=True)
class IntentResolution:
    raw_text: str
    normalized_text: str
    product: str | None
    quantity: int | None
    fulfillment: str | None
    missing: tuple[str, ...]
    questions: tuple[str, ...]

    @property
    def can_build_draft(self) -> bool:
        return self.product is not None and self.quantity is not None and self.fulfillment is not None

def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in value if not unicodedata.combining(ch))

def resolve_intent(text: str) -> IntentResolution:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("intent text is required")
    normalized = _normalize(text)
    product = None
    for canonical, variants in PRODUCTS.items():
        if any(re.search(r"\b" + re.escape(_normalize(term)) + r"\b", normalized)
               for term in variants):
            product = canonical
            break

    quantity = None
    digit = re.search(r"\b([1-9][0-9]?)\b", normalized)
    if digit:
        quantity = int(digit.group(1))
    else:
        words = {"una": 1, "uno": 1, "un": 1, "dos": 2, "tres": 3,
                 "cuatro": 4, "cinco": 5, "seis": 6}
        for word, value in words.items():
            if re.search(r"\b" + word + r"\b", normalized):
                quantity = value
                break
    if quantity is None and product:
        # A singular product noun is a linguistic quantity, not a product preference.
        singular = {"pizza", "hamburguesa", "cafe", "agua"}
        if product in singular:
            quantity = 1

    has_delivery = any(term in normalized for term in DELIVERY_TERMS)
    has_pickup = any(term in normalized for term in PICKUP_TERMS)
    fulfillment = "delivery" if has_delivery and not has_pickup else (
        "pickup" if has_pickup and not has_delivery else None
    )
    missing = []
    questions = []
    if product is None:
        missing.append("product")
        questions.append("¿Qué querés pedir?")
    if quantity is None:
        missing.append("quantity")
        questions.append("¿Cuántas unidades?")
    if fulfillment is None:
        missing.append("fulfillment")
        questions.append("¿Con entrega o retiro?")
    return IntentResolution(text, normalized, product, quantity, fulfillment,
                            tuple(missing), tuple(questions))
