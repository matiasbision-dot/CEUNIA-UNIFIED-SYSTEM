"""Show the merchant boundary without contacting any external service."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.proposal import create_proposal
from core.confirmation import record_confirmation
from core.merchant_adapter import MerchantCapability, validate_submission_boundary

def main() -> None:
    now = datetime.now(timezone.utc)
    proposal = create_proposal(merchant="Pizzeria Demo", region="Mar del Plata",
        product_id="pizza", product_name="Pizza mozzarella", quantity=1,
        modifiers=(), fulfillment="pickup", destination_id=None,
        unit_price=Decimal("8500"), currency="ARS", catalog_source="fixture_only",
        catalog_observed_at=now - timedelta(seconds=5), created_at=now,
        max_age_seconds=120)
    confirmation = record_confirmation(proposal,
        presented_proposal_id=proposal.proposal_id, decision="confirm",
        explicit_confirmation=True, decided_at=now)
    capability = MerchantCapability("Pizzeria Demo", "Mar del Plata",
        "sandbox", True, True, True)
    allowed, reason = validate_submission_boundary(proposal, confirmation,
        capability=capability, now=now, explicit_external_authorization=False)
    print("ONECLICK | FRONTERA COMERCIAL")
    print(f"Precondiciones: {reason}")
    print(f"Envío permitido: {allowed}")
    print("Comercio contactado: no")
    print("Pedido enviado: no")
    print("Pago realizado: no")
    print("La demostración no conecta ningún comercio.")

if __name__ == "__main__":
    main()