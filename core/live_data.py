"""Evidence and permission contract for the ONECLICK living-data economy.

This module validates incoming observations; it does not fetch, broker, sell,
or infer permission to use data. Connectors must provide source evidence.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import hashlib
import json

@dataclass(frozen=True)
class LiveDataRecord:
    source: str
    source_type: str
    observed_at: datetime
    expires_at: datetime
    purpose: str
    permission_granted: bool
    permission_scope: str
    quality_score: Decimal
    value: str
    unit: str = ""
    context_ref: str = ""

    def __post_init__(self):
        for name in ("source", "source_type", "purpose", "permission_scope", "value"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name}_required")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at_must_be_timezone_aware")
        if self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None:
            raise ValueError("expires_at_must_be_timezone_aware")
        if self.expires_at <= self.observed_at:
            raise ValueError("expiry_must_follow_observation")
        score = Decimal(str(self.quality_score))
        if not score.is_finite() or score < 0 or score > 1:
            raise ValueError("quality_score_must_be_between_zero_and_one")
        object.__setattr__(self, "quality_score", score)

    @property
    def record_id(self) -> str:
        payload = {
            "source": self.source, "source_type": self.source_type,
            "observed_at": self.observed_at.isoformat(),
            "expires_at": self.expires_at.isoformat(), "purpose": self.purpose,
            "permission_granted": self.permission_granted,
            "permission_scope": self.permission_scope,
            "quality_score": str(self.quality_score), "value": self.value,
            "unit": self.unit, "context_ref": self.context_ref,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class LiveDataAssessment:
    usable: bool
    reason: str
    record_id: str
    age_seconds: float | None = None

def assess_live_data(record: LiveDataRecord, *, now: datetime,
                     requested_purpose: str, minimum_quality: Decimal = Decimal("0.5")) -> LiveDataAssessment:
    """Fail closed unless source, purpose, permission, freshness and quality pass."""
    if not isinstance(record, LiveDataRecord):
        raise ValueError("live_data_record_required")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now_must_be_timezone_aware")
    if not isinstance(requested_purpose, str) or not requested_purpose.strip():
        raise ValueError("requested_purpose_required")
    threshold = Decimal(str(minimum_quality))
    if not threshold.is_finite() or threshold < 0 or threshold > 1:
        raise ValueError("minimum_quality_must_be_between_zero_and_one")
    age = (now - record.observed_at).total_seconds()
    if not record.permission_granted:
        return LiveDataAssessment(False, "permission_not_granted", record.record_id, age)
    if requested_purpose != record.purpose or requested_purpose != record.permission_scope:
        return LiveDataAssessment(False, "purpose_or_permission_scope_mismatch", record.record_id, age)
    if now < record.observed_at or now >= record.expires_at:
        return LiveDataAssessment(False, "observation_not_current", record.record_id, age)
    if record.quality_score < threshold:
        return LiveDataAssessment(False, "quality_below_threshold", record.record_id, age)
    return LiveDataAssessment(True, "live_data_usable_for_declared_purpose", record.record_id, age)

@dataclass(frozen=True)
class ResolutionValue:
    resolution_id: str
    data_record_ids: tuple[str, ...]
    outcome: str
    measured_value: Decimal
    currency_or_unit: str
    measured_at: datetime
    evidence_source: str

    def __post_init__(self):
        for name in ("resolution_id", "outcome", "currency_or_unit", "evidence_source"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name}_required")
        if not self.data_record_ids or any(not item.strip() for item in self.data_record_ids):
            raise ValueError("data_record_ids_required")
        value = Decimal(str(self.measured_value))
        if not value.is_finite():
            raise ValueError("measured_value_must_be_finite")
        object.__setattr__(self, "measured_value", value)
        if self.measured_at.tzinfo is None or self.measured_at.utcoffset() is None:
            raise ValueError("measured_at_must_be_timezone_aware")

    @property
    def is_measured_evidence(self) -> bool:
        return True
