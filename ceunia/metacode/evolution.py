"""CEUNIA MetaCode: evidence-aware evolution registry.

This module converts experiment reports into traceable records and bounded
next-step recommendations. It does not execute trades, launch agents, or
claim that reported results have been independently reproduced.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, default=str)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EvolutionDecision:
    experiment_id: str
    domain: str
    status: str
    point_albedrio: str
    metrics: dict[str, Any]
    evidence_grade: str
    next_action: str
    limitations: list[str]
    record_hash: str


def _finite_number(value: Any) -> Optional[float]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number != number or number in (float("inf"), float("-inf")):
        return None
    return number


def _valid_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _has_reproduction_metadata(reproduction: Any) -> bool:
    """Check metadata completeness only; this does not independently audit it."""
    if not isinstance(reproduction, Mapping):
        return False
    artifacts = reproduction.get("artifacts")
    return bool(
        reproduction.get("protocol_id")
        and reproduction.get("independent_reviewer")
        and reproduction.get("run_id")
        and isinstance(artifacts, list)
        and artifacts
        and all(
            isinstance(item, Mapping)
            and isinstance(item.get("path"), str)
            and item.get("path").strip()
            and _valid_sha256(item.get("sha256"))
            for item in artifacts
        )
    )


def evaluate_experiment(report: Mapping[str, Any]) -> EvolutionDecision:
    """Evaluate a report without upgrading evidence from a self-reported flag.

    Required keys: experiment_id, domain, baseline_mae, model_mae.
    Optional reproduction metadata must include protocol_id, independent_reviewer,
    run_id and artifacts [{path, sha256}]. Completeness is not an audit.
    """
    experiment_id = str(report.get("experiment_id", "")).strip()
    domain = str(report.get("domain", "")).strip().lower()
    if not experiment_id or not domain:
        raise ValueError("experiment_id y domain son obligatorios")

    baseline = _finite_number(report.get("baseline_mae"))
    model = _finite_number(report.get("model_mae"))
    walkforward = _finite_number(report.get("walkforward_mae"))
    test_n = report.get("test_n")
    if baseline is None or model is None or baseline <= 0 or model < 0:
        raise ValueError("baseline_mae debe ser > 0 y model_mae debe ser >= 0")
    if walkforward is not None and walkforward < 0:
        raise ValueError("walkforward_mae debe ser >= 0")
    if isinstance(test_n, bool) or (test_n is not None and
                                    (not isinstance(test_n, int) or test_n <= 0)):
        raise ValueError("test_n debe ser un entero positivo")

    hashes = report.get("source_hashes", [])
    if hashes is None:
        hashes = []
    if not isinstance(hashes, list) or not all(_valid_sha256(item) for item in hashes):
        raise ValueError("source_hashes debe contener SHA-256 hexadecimales de 64 caracteres")

    improvement = 100.0 * (baseline - model) / baseline
    wf_improvement = (
        100.0 * (baseline - walkforward) / baseline
        if walkforward is not None else None
    )
    wf_vs_model = (
        100.0 * (model - walkforward) / model
        if walkforward is not None and model > 0 else None
    )

    reproduction_complete = _has_reproduction_metadata(report.get("reproduction"))
    if improvement <= 0:
        evidence_grade = (
            "REPRODUCTION_METADATA_COMPLETE_PENDING_AUDIT"
            if reproduction_complete else "REPORTED_RESULT"
        )
        status = "NO_IMPROVEMENT"
        point = "HOLD_AND_REVIEW"
        next_action = "Investigate the absence of improvement; do not advance to a pilot."
    elif reproduction_complete:
        evidence_grade = "REPRODUCTION_METADATA_COMPLETE_PENDING_AUDIT"
        status = "IMPROVEMENT_REPORTED_REPRODUCTION_AUDIT_PENDING"
        point = "INDEPENDENT_REPRODUCTION_AUDIT"
        next_action = "Audit the reproduction protocol, reviewer independence and artifacts before any pilot."
    else:
        evidence_grade = "REPORTED_RESULT_NOT_INDEPENDENTLY_REPRODUCED"
        status = "REPORTED_IMPROVEMENT_PENDING_REPRODUCTION"
        point = "REPRODUCE_ON_EXISTING_ARTIFACTS"
        next_action = "Re-run the existing pipeline independently on saved artifacts; preserve current results."

    metrics = {
        "baseline_mae": baseline,
        "model_mae": model,
        "model_mae_improvement_pct": round(improvement, 6),
        "walkforward_mae": walkforward,
        "walkforward_vs_baseline_improvement_pct": (
            round(wf_improvement, 6) if wf_improvement is not None else None
        ),
        "walkforward_vs_model_mae_reduction_pct": (
            round(wf_vs_model, 6) if wf_vs_model is not None else None
        ),
        "test_n": test_n,
        "configurations_passed": report.get("configurations_passed"),
        "configurations_total": report.get("configurations_total"),
        "source_hashes_count": len(hashes),
    }
    limitations = [
        "Unreported evidence is not inferred.",
        "Reported improvement is not proof of universal superiority.",
        "Prediction quality does not by itself establish commercial value or investment returns.",
        "Reproduction metadata completeness is not independent verification of artifacts or reviewer independence.",
        "Triads and agents are not marked active unless execution logs prove it.",
    ]
    # The record fingerprint covers stable content only. Timestamp is metadata,
    # not part of the content identity, so identical records hash identically.
    payload = {
        "schema": "CEUNIA-CER-EVOLUTION-1.1",
        "experiment_id": experiment_id,
        "domain": domain,
        "status": status,
        "point_albedrio": point,
        "metrics": metrics,
        "evidence_grade": evidence_grade,
        "next_action": next_action,
        "limitations": limitations,
        "source": report.get("source"),
        "period": report.get("period"),
        "source_hashes": hashes,
        "reproduction": report.get("reproduction"),
        "notes": report.get("notes", []),
    }
    digest = sha256_json(payload)
    return EvolutionDecision(
        experiment_id=experiment_id,
        domain=domain,
        status=status,
        point_albedrio=point,
        metrics=metrics,
        evidence_grade=evidence_grade,
        next_action=next_action,
        limitations=limitations,
        record_hash=digest,
    )


def build_cer_bundle(reports: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Build a combined CER bundle for experiment reports."""
    decisions = [asdict(evaluate_experiment(item)) for item in reports]
    bundle = {
        "schema": "CEUNIA-CER-BUNDLE-1.1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "experiment_count": len(decisions),
        "decisions": decisions,
        "evolution_policy": {
            "preserve_positive_results": True,
            "record_errors_and_limitations": True,
            "meta_observation_before_irreversible_action": True,
            "finance_execution": "research_only_no_trading",
            "triads_state": "DESIGNED_NOT_ACTIVE_UNLESS_LOGGED",
        },
    }
    bundle["bundle_sha256"] = sha256_json(bundle)
    return bundle
