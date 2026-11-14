# Registro de proveedores e integraciones — CEUNIA Ω / ONECLICK

**Versión:** 0.1  
**Estado:** inventario inicial de objetivos; no acredita acuerdos, APIs habilitadas ni integraciones operativas.  
**Criterio:** una marca mencionada como posible proveedor no se considera conectada hasta contar con documentación oficial vigente, acceso autorizado, adaptador implementado y pruebas reproducibles.

## 1. Estados normalizados

| Estado | Significado | Evidencia mínima |
|---|---|---|
| IDENTIFICADO | Proveedor objetivo nombrado | Registro de oportunidad |
| INVESTIGACIÓN_PENDIENTE | Falta verificar API, país, producto y condiciones | Documentación oficial localizada y fechada |
| ACCESO_PENDIENTE | API/documentación viable, faltan credenciales o autorización | Alta aprobada por el proveedor |
| EN_DESARROLLO | Adaptador en construcción | Código y revisión |
| SANDBOX_VERIFICADO | Flujo probado con entorno y datos de prueba del proveedor | Logs y pruebas reproducibles |
| PRODUCCIÓN_VERIFICADA | Flujo real autorizado y validado | Evidencia de operación, permisos y controles |
| BLOQUEADO | Restricción técnica, comercial, legal o geográfica | Motivo y fecha de revisión |

## 2. Inventario inicial

Los nombres siguientes son objetivos de investigación derivados del alcance de ONECLICK. **No implican que exista API pública, acceso disponible ni integración.** La disponibilidad debe comprobarse para Argentina y para el producto concreto.

| Área | Proveedor objetivo | Estado | Próxima comprobación |
|---|---|---|---|
| Pedidos de comida | PedidosYa | IDENTIFICADO | Canales oficiales para comercios/partners, API y cobertura Argentina |
| Pedidos de comida | Rappi | IDENTIFICADO | Programa de partners, API autorizada y condiciones |
| Movilidad | Uber | IDENTIFICADO | APIs aplicables a solicitud de viajes, elegibilidad y límites |
| Movilidad | Cabify | IDENTIFICADO | Integración empresarial/partners y cobertura |
| Movilidad | DiDi | IDENTIFICADO | Acceso oficial para integradores y cobertura |
| Pagos | Mercado Pago | IDENTIFICADO | Checkout/API oficial, credenciales de prueba, webhooks y obligaciones |
| Pagos | Stripe | IDENTIFICADO | Disponibilidad del servicio para la entidad y país de operación |
| Pagos | PayPal | IDENTIFICADO | API oficial, elegibilidad y flujo de autorización |
| Mensajería | WhatsApp Business Platform | IDENTIFICADO | API oficial, plantillas, consentimiento y costos |
| Mensajería | Telegram | IDENTIFICADO | Bot API, permisos y límites |
| IA | OpenAI | IDENTIFICADO | API oficial, permisos, costos y tratamiento de datos |
| IA | Anthropic | IDENTIFICADO | API oficial, permisos, costos y tratamiento de datos |
| IA | Google Gemini | IDENTIFICADO | API oficial, permisos, costos y tratamiento de datos |

## 3. Capacidades que debe registrar cada proveedor

Cada ficha verificable debe incluir:

- Identidad legal/comercial y URL de documentación oficial.
- Producto/API exacto, versión y fecha de consulta.
- Países, ciudades y categorías cubiertas.
- Operaciones permitidas: catálogo, cotización, disponibilidad, reserva, pedido, pago, cancelación, seguimiento y reembolso.
- Autenticación, scopes, roles y titular de las credenciales.
- Entornos disponibles: sandbox, test y producción.
- Tarifas, comisiones, límites, SLA y restricciones contractuales.
- Datos personales tratados, retención, transferencias y requisitos de consentimiento.
- Webhooks, idempotencia, reintentos y conciliación.
- Estado CEUNIA, evidencia enlazada, responsable y próxima revisión.

No completar campos desconocidos por inferencia. Usar explícitamente PENDIENTE o NO_VERIFICADO.

## 4. Brecha técnica actual

El núcleo del repositorio dispone de:

- Contrato `ProviderAdapter` con método `quote(intent, region)`.
- `Capability` con indicadores `supports_quote` y `supports_order`.
- `DemoAdapter` restringido a datos sandbox.
- Orquestación de cotizaciones y ranking.
- Puerta de consentimiento para una solicitud de acción.

Pero todavía **no** dispone de un contrato de ejecución de pedidos, adaptadores de proveedores reales, gestión de credenciales, webhooks, conciliación, cancelación ni pruebas de producción. El campo `supports_order` no constituye por sí solo una capacidad de compra.

Por lo tanto, el estado real es: **comparación sandbox demostrable; pedido real no implementado**.

## 5. Puerta de activación ONECLICK

Una operación real no debe ejecutarse hasta superar, en este orden:

1. Intención interpretada y resumida para revisión.
2. Proveedor y operación admitidos en la región.
3. Cotización/disponibilidad vigente con moneda, cargos y vencimiento.
4. Restricciones, presupuesto y preferencias verificadas.
5. Resumen final visible: proveedor, producto/servicio, importe total, destino y condiciones.
6. Consentimiento explícito para esa operación concreta.
7. Clave de idempotencia y protección contra duplicados.
8. Ejecución mediante API oficial y credenciales autorizadas.
9. Confirmación del proveedor con identificador externo.
10. Registro de resultado, recibo, errores y opción de soporte/cancelación.

Si una condición crítica no se verifica, CEUNIA debe CONSULTAR o ABSTENERSE, nunca simular una compra exitosa.

## 6. Próxima prioridad de implementación

Antes de integrar múltiples marcas, construir un único flujo vertical de extremo a extremo con un proveedor que autorice el acceso:

- ficha de capacidad verificable;
- contrato separado para cotizar y ejecutar;
- entorno de prueba oficial;
- consentimiento vinculado a importe y operación;
- idempotencia, logs y pruebas de fallo;
- demostración reproducible y documentación de límites.

La selección del primer proveedor queda pendiente de comprobar acceso oficial, viabilidad en Argentina y condiciones comerciales. No se presume disponibilidad.

---
**Principio rector:** ONECLICK reduce la expresión y los pasos del usuario; no reduce la claridad, el consentimiento ni la trazabilidad.
