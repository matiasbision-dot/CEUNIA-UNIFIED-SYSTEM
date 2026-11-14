"""Demonstrate explicit confirmation recording without merchant submission."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.proposal import create_proposal
from core.confirmation import record_confirmation

def main() -> None:
    now = datetime.now(timezone.utc)
    proposal = create_proposal(
        merchant="Pizzeria Demo (sandbox)", region="Mar del Plata",
        product_id="pizza-mozz", product_name="Pizza mozzarella",
        quantity=1, modifiers=(), fulfillment="pickup", destination_id=None,
        unit_price=Decimal("8500"), currency="ARS",
        catalog_source="fixture_not_live_merchant",
        catalog_observed_at=now - timedelta(seconds=5), created_at=now,
        max_age_seconds=120)
    record = record_confirmation(
        proposal, presented_proposal_id=proposal.proposal_id,
        decision="confirm", explicit_confirmation=True,
        decided_at=now)
    print("ONECLICK | CONFIRMACIÓN HUMANA")
    print(f"Propuesta: {record.proposal_id}")
    print(f"Decisión: {record.decision}")
    print(f"Estado: {record.status}")
    print(f"ID de confirmación: {record.confirmation_id}")
    print(f"Ejecución autorizada: {record.execution_authorized}")
    print(f"Pedido enviado: {record.order_submitted}")
    print(f"Pago realizado: {record.payment_taken}")
    print("La confirmación registra la decisión; no envía el pedido.")

if __name__ == "__main__":
    main()
