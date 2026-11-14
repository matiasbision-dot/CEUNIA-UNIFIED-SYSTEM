"""Runnable ONECLICK -> CEUNIA Ω demo using fictional sandbox quotes only.

Run from repository root:
    python -m examples.oneclick_sandbox
"""
from core.adapters import Capability, DemoAdapter, Quote
from core.orchestrator import compare_providers

def main() -> None:
    adapters = [
        DemoAdapter(
            Capability("Proveedor A (SIMULADO)", "food", "Mar del Plata", True, False, "sandbox"),
            Quote("Proveedor A (SIMULADO)", 8500, "ARS", 25, True, "fixture-local", "sandbox"),
        ),
        DemoAdapter(
            Capability("Proveedor B (SIMULADO)", "food", "Mar del Plata", True, False, "sandbox"),
            Quote("Proveedor B (SIMULADO)", 9200, "ARS", 18, True, "fixture-local", "sandbox"),
        ),
    ]
    decision = compare_providers("pizza", "Mar del Plata", adapters)
    print("CEUNIA Ω | ONECLICK SANDBOX")
    print("Intención: pizza")
    print("Región: Mar del Plata")
    print(f"Estado: {decision.status}")
    print(f"Motivo: {decision.reason}")
    for position, item in enumerate(decision.ranked, start=1):
        offer = item.offer
        print(f"{position}. {offer.provider}: ${offer.price:.2f} {offer.currency} | {offer.minutes:g} min | score={item.score:.4f}")
    print(f"Ejecución externa realizada: {decision.execution_performed}")
    print("Nota: cotizaciones ficticias de sandbox; no se contactó a ningún comercio.")

if __name__ == "__main__":
    main()