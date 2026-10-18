"""Evidence-based CEUNIA decision gate (v2).

This module validates structured decision records. It does not claim to
understand arbitrary natural-language content or replace domain review.
Missing/invalid inputs fail closed to HOLD.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List
import hashlib
import json


@dataclass(frozen=True)
class ValidationPolicy:
    max_risk: float = 0.35
    max_uncertainty: float = 0.40
    min_evidence_quality: float = 0.60


class CEUNIAEvidenceValidator:
    def __init__(self, policy: ValidationPolicy = ValidationPolicy()):
        self.policy = policy
        self.history: List[Dict[str, Any]] = []

    @staticmethod
    def _unit_interval(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and 0.0 <= float(value) <= 1.0

    def evaluate(self, record: Any) -> Dict[str, Any]:
        reasons: List[str] = []
        if not isinstance(record, dict):
            record = {}
            reasons.append("record_must_be_object")

        objective = record.get("objective")
        evidence = record.get("evidence")
        risk = record.get("risk_score")
        uncertainty = record.get("uncertainty_score")
        evidence_quality = record.get("evidence_quality")

        if not isinstance(objective, str) or not objective.strip():
            reasons.append("missing_objective")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
            reasons.append("missing_or_invalid_evidence")
        if not self._unit_interval(risk):
            reasons.append("risk_score_must_be_0_to_1")
        if not self._unit_interval(uncertainty):
            reasons.append("uncertainty_score_must_be_0_to_1")
        if not self._unit_interval(evidence_quality):
            reasons.append("evidence_quality_must_be_0_to_1")

        if not reasons:
            if float(risk) > self.policy.max_risk:
                reasons.append("risk_above_policy")
            if float(uncertainty) > self.policy.max_uncertainty:
                reasons.append("uncertainty_above_policy")
            if float(evidence_quality) < self.policy.min_evidence_quality:
                reasons.append("evidence_quality_below_policy")

        status = "APPROVE" if not reasons else "HOLD"
        result = {
            "status": status,
            "reasons": reasons,
            "policy": asdict(self.policy),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "record_sha256": hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest(),
        }
        self.history.append(result)
        return result

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self.history)


def validate_evidence(record: Any) -> Dict[str, Any]:
    return CEUNIAEvidenceValidator().evaluate(record)
