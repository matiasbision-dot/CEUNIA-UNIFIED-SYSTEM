# ONECLICK — Especificación de catálogo del comercio
**Versión:** 0.1 · **Estado:** especificación; sin catálogo real conectado

## 1. Propósito
Definir el formato mínimo para recibir, validar y mostrar catálogo, precios y disponibilidad de un comercio autorizado. No contiene productos ni precios reales. Los ejemplos son ilustrativos y no deben utilizarse como oferta.

## 2. Campos mínimos por artículo
| Campo | Tipo | Regla |
|---|---|---|
| merchant_id | string | Identificador estable asignado al comercio |
| item_id | string | Identificador estable dentro del comercio |
| name | string | Nombre visible no vacío |
| description | string/null | Descripción autorizada |
| price_amount | decimal string | Decimal exacto, no float binario |
| currency | string | Código ISO 4217 validado en implementación |
| available | boolean/unknown | Unknown no se interpreta como disponible |
| valid_from | ISO-8601 | Inicio de vigencia con zona horaria |
| valid_until | ISO-8601/null | Fin exclusivo de vigencia |
| source_id | string | Fuente autorizada de origen |
| source_record_id | string | Identidad del registro de origen |
| retrieved_at | ISO-8601 | Momento de consulta |
| modifiers | array | Opciones y reglas explícitas |
| fulfillment | object | Retiro/delivery y restricciones |

## 3. Precio y moneda
- Usar cadenas decimales, por ejemplo `"12500.00"`, para evitar errores de punto flotante.
- Registrar moneda explícitamente en cada precio.
- No sumar importes de monedas distintas.
- Separar precio base, adicionales, descuentos, impuestos, cargos de entrega y total.
- El total de una propuesta debe reconstruirse desde sus componentes y reglas.
- Si falta un cargo o no puede calcularse el total comparable, marcar precio como incompleto y no afirmar mejora económica.

## 4. Modificadores
Cada modificador define: `modifier_id`, nombre, selección mínima/máxima, opciones, diferencia de precio, disponibilidad y compatibilidad. No inferir ingredientes, tamaños, cantidades, promociones ni sustituciones que el comercio no haya informado.

## 5. Disponibilidad y vigencia
- La ausencia de información no significa disponibilidad.
- Un precio vencido no se presenta como vigente.
- Una consulta fallida o fuente desactualizada genera estado UNKNOWN/STALE y abstención de oferta firme.
- Cada respuesta conserva `retrieved_at`, `valid_from`, `valid_until` y referencia de fuente.
- Definir por comercio el TTL máximo: [PENDIENTE DE ACUERDO].
- Las diferencias entre horarios publicados y disponibilidad puntual deben mostrarse como tales, sin inferir stock.

## 6. Modalidad de entrega
Registrar por separado:
- retiro en local: habilitado, horarios, dirección e instrucciones;
- delivery: habilitado, zonas, mínimo, tarifa, tiempo estimado y restricciones;
- cargos y condiciones de cada modalidad;
- estado desconocido cuando no haya confirmación.

No transformar retiro en delivery ni delivery en retiro por conveniencia del sistema.

## 7. Validaciones y rechazo
Rechazar o poner en cuarentena registros con identificadores duplicados, precio negativo, moneda ausente/inválida, fechas incoherentes, fuente no autorizada, campos obligatorios vacíos o modificadores contradictorios. Los importes cero requieren regla explícita y evidencia.

## 8. Ejemplo exclusivamente ficticio
```json
{
  "merchant_id": "DEMO_ONLY",
  "item_id": "PIZZA_DEMO_001",
  "name": "Pizza de ejemplo",
  "price_amount": "12500.00",
  "currency": "ARS",
  "available": null,
  "valid_from": "2026-01-01T00:00:00-03:00",
  "valid_until": null,
  "source_id": "FIXTURE_NOT_LIVE",
  "source_record_id": "demo-record-001",
  "retrieved_at": "2026-01-01T12:00:00-03:00",
  "modifiers": [],
  "fulfillment": {"pickup": "unknown", "delivery": "unknown"}
}
```
Este registro no representa un comercio, precio ni disponibilidad reales.

## 9. Checklist de incorporación
- [ ] Autorización vigente y firmada.
- [ ] Fuente y campos permitidos documentados.
- [ ] Moneda y formato decimal validados.
- [ ] Vigencia/TTL acordados.
- [ ] Reglas de modificadores documentadas.
- [ ] Retiro/delivery y cargos documentados.
- [ ] Pruebas de registros vencidos, ausentes y contradictorios.
- [ ] Evidencia de origen conservada.
