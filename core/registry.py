"""Evidence-aware registry for provider capabilities; unknowns stay explicit."""
from dataclasses import dataclass, field
from datetime import date
from typing import Iterable

VALID_STATUSES = {
    "IDENTIFICADO", "INVESTIGACION_PENDIENTE", "ACCESO_PENDIENTE",
    "EN_DESARROLLO", "SANDBOX_VERIFICADO", "PRODUCCION_VERIFICADA", "BLOQUEADO",
}
VALID_ENVIRONMENTS = {"unknown", "sandbox", "test", "production"}

@dataclass(frozen=True)
class ProviderRecord:
    provider: str
    category: str
    region: str
    status: str = "IDENTIFICADO"
    operations: frozenset[str] = field(default_factory=frozenset)
    environment: str = "unknown"
    documentation_url: str | None = None
    checked_on: date | None = None
    evidence: tuple[str, ...] = ()

    def __post_init__(self):
        if not self.provider.strip() or not self.category.strip() or not self.region.strip():
            raise ValueError("provider, category and region are required")
        if self.status not in VALID_STATUSES:
            raise ValueError("invalid provider status")
        if self.environment not in VALID_ENVIRONMENTS:
            raise ValueError("invalid environment")
        if self.status in {"SANDBOX_VERIFICADO", "PRODUCCION_VERIFICADA"} and not self.evidence:
            raise ValueError("verified status requires evidence")
        if self.status == "PRODUCCION_VERIFICADA" and self.environment != "production":
            raise ValueError("production status requires production environment")
        if self.status == "SANDBOX_VERIFICADO" and self.environment != "sandbox":
            raise ValueError("sandbox status requires sandbox environment")
        if self.documentation_url and not self.documentation_url.startswith("https://"):
            raise ValueError("documentation URL must use HTTPS")

def validate_registry(records: Iterable[ProviderRecord]) -> tuple[ProviderRecord, ...]:
    """Return a stable provider list and reject duplicate provider/category/region keys."""
    result = tuple(records)
    keys = [(r.provider.casefold(), r.category.casefold(), r.region.casefold()) for r in result]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate provider/category/region record")
    return tuple(sorted(result, key=lambda r: (r.category, r.provider.casefold(), r.region)))
