"""Demonstrate one-line Spanish intent capture and minimal clarification."""
from core.intent import resolve_intent

def main() -> None:
    sample = "Quiero una pizza"
    result = resolve_intent(sample)
    print("ONECLICK | CAPTURA DE INTENCIÓN")
    print(f"Entrada: {result.raw_text}")
    print(f"Producto: {result.product or 'sin identificar'}")
    print(f"Cantidad: {result.quantity if result.quantity is not None else 'sin especificar'}")
    print(f"Entrega/retiro: {result.fulfillment or 'sin especificar'}")
    if result.questions:
        print("Siguiente pregunta:")
        print(result.questions[0])
    print("Comercio, variante, precio y dirección: pendientes de selección/verificación.")
    print("Pedido realizado: no")

if __name__ == "__main__":
    main()
