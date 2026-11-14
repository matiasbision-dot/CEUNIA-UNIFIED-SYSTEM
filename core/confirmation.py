"""Human confirmation records for ONECLICK proposals.

This module records a user's explicit decision about the exact proposal shown.
It does NOT submit an order, contact a merchant, reserve stock or charge money.
"""
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from .proposal import OrderProposal

@dataclass(frozen=True)
class ConfirmationRecord:
    confirmation_id: str
    proposal_id: str
    decision: str
    status: str
    decided_at: datetime
    execution_authorized: bool = False
    order_submitted: bool = False
    payment_taken: bool = False

def record_confirmation(proposal: OrderProposal, *,
                        presented_proposal_id: str,
                        decision: str,
                        explicit_confirmation: bool,
                        decided_at: datetime) -> ConfirmationRecord:
    """Record confirm/decline for the exact, still-valid proposal shown to user."""
    if not isinstance(proposal, OrderProposal):
        raise ValueError("valid_order_proposal_required")
    if presented_proposal_id != proposal.proposal_id:
        raise ValueError("presented_proposal_mismatch")
    if decision not in ("confirm", "decline"):
        raise ValueError("decision_must_be_confirm_or_decline")
    if not isinstance(explicit_confirmation, bool) or not explicit_confirmation:
        raise ValueError("explicit_user_decision_required")
    if decided_at.tzinfo is None or decided_at.utcoffset() is None:
        raise ValueError("decision_timestamp_must_be_timezone_aware")
    if decided_at < proposal.created_at:
        raise ValueError("decision_precedes_proposal")
    if decided_at > proposal.valid_until:
        raise ValueError("proposal_expired_refresh_required")
    if proposal.submitted or proposal.paid:
        raise ValueError("proposal_already_submitted_or_paid")
    status = "CONFIRMED_FOR_NEXT_STEP" if decision == "confirm" else "DECLINED"
    payload = {
        "proposal_id": proposal.proposal_id,
        "decision": decision,
        "decided_at": decided_at.isoformat(),
    }
    confirmation_id = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return ConfirmationRecord(
        confirmation_id=confirmation_id,
        proposal_id=proposal.proposal_id,
        decision=decision,
        status=status,
        decided_at=decided_at,
    )
