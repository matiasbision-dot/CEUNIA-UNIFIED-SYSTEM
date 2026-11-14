"""Demonstrate live-data admissibility without fetching external data."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from core.live_data import LiveDataRecord, assess_live_data

def main():
    now = datetime.now(timezone.utc)
    record = LiveDataRecord(source="sandbox_fixture", source_type="merchant_catalog",
        observed_at=now-timedelta(seconds=3), expires_at=now+timedelta(minutes=2),
        purpose="prepare_quote", permission_granted=True, permission_scope="prepare_quote",
        quality_score=Decimal("0.95"), value="8500.00", unit="ARS",
        context_ref="sandbox:pizzeria-demo")
    result = assess_live_data(record, now=now, requested_purpose="prepare_quote")
    print("ALL I | ECONOMÍA DE DATOS VIVOS")
    print(f"Registro: {result.record_id}")
    print(f"Admisible: {result.usable}")
    print(f"Evaluación: {result.reason}")
    print("Origen externo consultado: no")
    print("Permiso real de un comercio: no; fixture de demostración")
    print("Datos personales: no")

if __name__ == "__main__":
    main()