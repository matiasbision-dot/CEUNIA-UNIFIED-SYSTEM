"""Demonstrate durable ONECLICK proposal and decision history using SQLite."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from core.proposal import create_proposal
from core.confirmation import record_confirmation
from core.confirmation_store import ConfirmationStore

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
    decision = record_confirmation(
        proposal, presented_proposal_id=proposal.proposal_id,
        decision="confirm", explicit_confirmation=True, decided_at=now)
    with TemporaryDirectory() as directory:
        store = ConfirmationStore(Path(directory) / "oneclick.sqlite3")
        store.save_proposal(proposal)
        store.record_decision(decision)
        store.record_outcome(
            proposal_id=proposal.proposal_id, outcome="demo_recorded",
            source="local_sandbox_demo", observed_at=now,
            idempotency_key="demo-event-001", details={"simulated": True})
        history = ConfirmationStore(Path(directory) / "oneclick.sqlite3").get_history(
            proposal.proposal_id)
        print("ONECLICK | MEMORIA SQLITE")
        print(f"Propuesta: {history['proposal']['proposal_id']}")
        print(f"Decisión: {history['confirmation']['status']}")
        print(f"Eventos persistidos: {len(history['outcomes'])}")
        print("Base SQLite reabierta: sí")
        print("Comercio contactado: no")
        print("Pedido enviado: no")
        print("Pago realizado: no")
        print("DATOS SIMULADOS: demostración local, no operación comercial.")

if __name__ == "__main__":
    main()
