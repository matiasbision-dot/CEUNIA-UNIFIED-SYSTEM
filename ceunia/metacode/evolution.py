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


def evaluate_experiment(report: Mapping[str, Any]) -> EvolutionDecision:
    """Evaluate a report without upgrading its evidence status by assumption.

    Required keys: experiment_id, domain, baseline_mae, model_mae.
    Optional: walkforward_mae, test_n, source, period, reproduced,
    source_hashes, notes.
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

    improvement = 100.0 * (baseline - model) / baseline
    wf_improvement = (
        100.0 * (baseline - walkforward) / baseline
        if walkforward is not None else None
    )
    wf_vs_model = (
        100.0 * (model - walkforward) / model
        if walkforward is not None and model > 0 else None
    )

    reproduced = bool(report.get("reproduced", False))
    hashes = report.get("source_hashes") or []
    if reproduced and hashes and isinstance(test_n, int) and test_n > 0:
        evidence_grade = "REPRODUCED_WITH_ARTIFACTS"
        status = "REPRODUCED_IMPROVEMENT" if improvement > 0 else "NO_IMPROVEMENT"
    elif improvement > 0:
        evidence_grade = "REPORTED_RESULT_NOT_INDEPENDENTLY_REPRODUCED"
        status = "REPORTED_IMPROVEMENT_PENDING_REPRODUCTION"
    else:
        evidence_grade = "REPORTED_RESULT"
        status = "NO_REPORTED_MAE_IMPROVEMENT"

    if not report.get("source") or not report.get("period"):
        point = "COMPLETE_SOURCE_AND_PERIOD_METADATA"
        next_action = "Attach source, period, preprocessing, split definition, and artifact hashes."
    elif not reproduced:
        point = "REPRODUCE_ON_EXISTING_ARTIFACTS"
        next_action = "Re-run the existing pipeline on the saved artifacts; preserve current results."
    else:
        point = "TRANSFER_TO_SHADOW_PILOT"
        next_action = "Run a bounded shadow-mode pilot and compare against the operational baseline."

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
    payload = {
        "schema": "CEUNIA-CER-EVOLUTION-1.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "experiment_id": experiment_id,
        "domain": domain,
        "status": status,
        "point_albedrio": point,
        "metrics": metrics,
        "evidence_grade": evidence_grade,
        "next_action": next_action,
        "limitations": [
            "Unreported evidence is not inferred.",
            "Reported improvement is not proof of universal superiority.",
            "Prediction quality does not by itself establish commercial value or investment returns.",
            "Triads and agents are not marked active unless execution logs prove it.",
        ],
        "source": report.get("source"),
        "period": report.get("period"),
        "source_hashes": hashes,
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
        limitations=payload["limitations"],
        record_hash=digest,
    )


def build_cer_bundle(reports: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Build a combined CER bundle for NASA and finance reports."""
    decisions = [asdict(evaluate_experiment(item)) for item in reports]
    bundle = {
        "schema": "CEUNIA-CER-BUNDLE-1.0",
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
