"""Merchant adapter contracts and guarded ONECLICK submission boundary.

No live merchant implementation is included. Production adapters must be
separately authorized, reviewed and tested against the merchant contract.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from .proposal import OrderProposal
from .confirmation import ConfirmationRecord

@dataclass(frozen=True)
class MerchantCapability:
    merchant: str
    region: str
    environment: str
    supports_catalog: bool
    supports_order_submission: bool
    supports_idempotency: bool

@dataclass(frozen=True)
class MerchantSubmission:
    merchant: str
    merchant_order_id: str
    status: str
    source: str
    observed_at: datetime
    idempotency_key: str

class MerchantAdapter(Protocol):
    capability: MerchantCapability
    def submit_order(self, proposal: OrderProposal, *,
                     confirmation: ConfirmationRecord,
                     idempotency_key: str) -> MerchantSubmission: ...

def validate_submission_boundary(proposal: OrderProposal,
                                 confirmation: ConfirmationRecord, *,
                                 capability: MerchantCapability,
                                 now: datetime,
                                 explicit_external_authorization: bool) -> tuple[bool, str]:
    """Validate every precondition without making a network call."""
    if not isinstance(proposal, OrderProposal):
        return False, "valid_order_proposal_required"
    if not isinstance(confirmation, ConfirmationRecord):
        return False, "valid_confirmation_record_required"
    if confirmation.proposal_id != proposal.proposal_id:
        return False, "confirmation_proposal_mismatch"
    if confirmation.decision != "confirm" or confirmation.status != "CONFIRMED_FOR_NEXT_STEP":
        return False, "explicit_confirmation_required"
    if confirmation.execution_authorized or confirmation.order_submitted or confirmation.payment_taken:
        return False, "confirmation_record_has_invalid_execution_flags"
    if not explicit_external_authorization:
        return False, "external_execution_authorization_required"
    if now.tzinfo is None or now.utcoffset() is None:
        return False, "current_timestamp_must_be_timezone_aware"
    if now < proposal.created_at or now > proposal.valid_until:
        return False, "proposal_expired_or_not_yet_valid"
    if proposal.submitted or proposal.paid:
        return False, "proposal_already_submitted_or_paid"
    if not isinstance(capability, MerchantCapability):
        return False, "merchant_capability_required"
    if capability.merchant != proposal.merchant:
        return False, "merchant_identity_mismatch"
    if capability.region != proposal.region:
        return False, "merchant_region_mismatch"
    if capability.environment != "production":
        return False, "production_adapter_required"
    if not capability.supports_order_submission:
        return False, "merchant_order_submission_not_supported"
    if not capability.supports_idempotency:
        return False, "merchant_idempotency_required"
    return True, "submission_preconditions_met"

def submit_confirmed_order(adapter: MerchantAdapter, proposal: OrderProposal,
                           confirmation: ConfirmationRecord, *,
                           now: datetime, idempotency_key: str,
                           explicit_external_authorization: bool = False) -> MerchantSubmission:
    """Submit only after all checks; adapter must enforce idempotency remotely.

    This function makes a real external call when explicitly authorized and
    supplied with a production adapter. Tests use a local fake adapter only.
    """
    if not isinstance(idempotency_key, str) or not idempotency_key.strip():
        raise ValueError("merchant_idempotency_key_required")
    capability = getattr(adapter, "capability", None)
    allowed, reason = validate_submission_boundary(
        proposal, confirmation, capability=capability, now=now,
        explicit_external_authorization=explicit_external_authorization)
    if not allowed:
        raise PermissionError(reason)
    result = adapter.submit_order(proposal, confirmation=confirmation,
                                  idempotency_key=idempotency_key)
    if not isinstance(result, MerchantSubmission):
        raise ValueError("invalid_merchant_submission_response")
    if result.merchant != proposal.merchant:
        raise ValueError("merchant_response_identity_mismatch")
    if result.idempotency_key != idempotency_key:
        raise ValueError("merchant_response_idempotency_mismatch")
    if result.observed_at.tzinfo is None or result.observed_at.utcoffset() is None:
        raise ValueError("merchant_response_timestamp_must_be_timezone_aware")
    if not result.merchant_order_id.strip() or not result.status.strip() or not result.source.strip():
        raise ValueError("merchant_response_fields_required")
    return result
