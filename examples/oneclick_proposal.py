"""Runnable, clearly simulated ONECLICK proposal demonstration."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.catalog import CatalogItem, CatalogSnapshot
from core.oneclick_flow import prepare_order

def main() -> None:
    now = datetime.now(timezone.utc)
    catalog = CatalogSnapshot(
        provider="Pizzeria Demo (sandbox)",
        region="Mar del Plata",
        currency="ARS",
        source="fixture_not_live_merchant",
        observed_at=now - timedelta(seconds=15),
        items=(CatalogItem("pizza-mozz", "Pizza mozzarella", Decimal("8500"),
                           True, ("extra queso", "sin aceitunas")),),
    )
    result = prepare_order(
        "Quiero una pizza", catalog=catalog, product_id="pizza-mozz",
        fulfillment="delivery", destination_id="demo-address-reference",
        now=now, max_catalog_age_seconds=120, merchant_available=True,
        budget_limit=Decimal("10000"),
    )
    print("ONECLICK | PROPUESTA PARA REVISIÓN")
    print(f"Estado: {result.status}")
    if result.proposal is None:
        print(f"Motivo: {result.reason}")
        return
    p = result.proposal
    print(f"ID: {p.proposal_id}")
    print(f"Comercio: {p.merchant}")
    print(f"Producto: {p.product_name} x{p.quantity}")
    print(f"Precio unitario: {p.unit_price} {p.currency}")
    print(f"Subtotal catálogo: {p.subtotal} {p.currency}")
    print(f"Modalidad: {p.fulfillment}")
    print(f"Fuente: {p.catalog_source}")
    print(f"Observado: {p.catalog_observed_at.isoformat()}")
    print(f"Válido hasta: {p.valid_until.isoformat()}")
    print("Confirmación requerida: sí")
    print("Compra enviada: no")
    print("Pago realizado: no")
    print("DATOS SIMULADOS: no es una cotización comercial real.")

if __name__ == "__main__":
    main()
