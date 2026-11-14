"""Verifiable economic-trial contract for a ONECLICK resolution.

This records comparable measurements. It does not fetch live data, establish
legal consent, submit orders, or assign monetary value to time/errors.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple


@dataclass(frozen=True)
class SourceContribution:
    source_id: str
    live_data_record_id: str
    contribution_evidence_ref: str

    def __post_init__(self):
        for field in ("source_id", "live_data_record_id", "contribution_evidence_ref"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field}_required")


@dataclass(frozen=True)
class EconomicTrial:
    trial_id: str
    resolution_id: str
    baseline_time_seconds: int
    oneclick_time_seconds: int
    baseline_error_count: int
    oneclick_error_count: int
    baseline_total: Decimal
    oneclick_total: Decimal
    currency: str
    outcome_status: str
    outcome_evidence_ref: str
    source_contributions: Tuple[SourceContribution, ...]
    distribution_status: str = "not_defined"
    distribution_terms_ref: str = ""

    def __post_init__(self):
        for field in ("trial_id", "resolution_id", "currency", "outcome_status",
                      "outcome_evidence_ref"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field}_required")
        for field in ("baseline_time_seconds", "oneclick_time_seconds",
                      "baseline_error_count", "oneclick_error_count"):
            value = getattr(self, field)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{field}_must_be_non_negative_integer")
        if self.baseline_time_seconds == 0:
            raise ValueError("baseline_time_must_be_positive")
        for field in ("baseline_total", "oneclick_total"):
            value = Decimal(str(getattr(self, field)))
            if not value.is_finite() or value < 0:
                raise ValueError(f"{field}_must_be_finite_non_negative")
            object.__setattr__(self, field, value)
        if not self.source_contributions:
            raise ValueError("at_least_one_source_contribution_required")
        source_ids = [item.source_id for item in self.source_contributions]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("duplicate_source_contribution")
        if self.distribution_status not in ("not_defined", "terms_authorized", "reconciled"):
            raise ValueError("distribution_status_invalid")
        if self.distribution_status in ("terms_authorized", "reconciled") and not self.distribution_terms_ref.strip():
            raise ValueError("authorized_distribution_terms_reference_required")
        if self.distribution_status == "reconciled" and self.outcome_status != "verified":
            raise ValueError("distribution_cannot_be_reconciled_without_verified_outcome")

    @property
    def time_saved_seconds(self) -> int:
        return self.baseline_time_seconds - self.oneclick_time_seconds

    @property
    def errors_avoided(self) -> int:
        return self.baseline_error_count - self.oneclick_error_count

    @property
    def price_improvement(self) -> Decimal:
        """Positive means cheaper than baseline; negative means more expensive."""
        return self.baseline_total - self.oneclick_total

    @property
    def price_improvement_percent(self) -> Decimal:
        if self.baseline_total == 0:
            return Decimal("0")
        return (self.price_improvement / self.baseline_total) * Decimal("100")

    @property
    def economic_claim_is_verified(self) -> bool:
        return self.outcome_status == "verified" and bool(self.outcome_evidence_ref.strip())

    def metrics(self) -> dict:
        return {
            "time_saved_seconds": self.time_saved_seconds,
            "errors_avoided": self.errors_avoided,
            "price_improvement": str(self.price_improvement),
            "price_improvement_percent": str(self.price_improvement_percent),
            "currency": self.currency,
            "source_count": len(self.source_contributions),
            "source_ids": [item.source_id for item in self.source_contributions],
            "outcome_verified": self.economic_claim_is_verified,
            "distribution_status": self.distribution_status,
            "distribution_terms_ref": self.distribution_terms_ref or None,
        }
