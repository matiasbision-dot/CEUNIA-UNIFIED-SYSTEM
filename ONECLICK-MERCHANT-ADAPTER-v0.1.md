# ONECLICK — Especificación del adaptador de comercio
**Versión:** 0.1 · **Estado:** diseño contractual; no acredita integración productiva

## 1. Objetivo
Establecer una frontera segura entre ONECLICK y un comercio autorizado. La primera fase permite consultar datos autorizados y construir propuestas. El adaptador debe denegar por defecto toda operación externa de escritura.

## 2. Modos
| Modo | Capacidades | Estado previsto |
|---|---|---|
| FIXTURE | Datos ficticios claramente etiquetados | Desarrollo/CI |
| READ_ONLY | Consulta de fuente autorizada | Piloto, tras autorización |
| PROPOSAL | Generación de propuesta sin envío | Piloto, tras autorización |
| EXECUTION | Envío externo de pedido | Deshabilitado; requiere anexo y aprobación separados |

No existe transición automática a EXECUTION. Cambiar el modo requiere revisión, configuración explícita, pruebas y evidencia de autorización.

## 3. Flujo de consulta y propuesta
1. Recibir intención del usuario.
2. Interpretar artículos, cantidades, modificadores y modalidad.
3. Detectar ambigüedades y preguntar antes de proponer.
4. Consultar únicamente fuentes autorizadas.
5. Validar procedencia, vigencia, disponibilidad y moneda.
6. Construir propuesta con detalle y total calculable.
7. Mostrar la propuesta para revisión humana.
8. Registrar aceptación/rechazo de la propuesta como evento interno.
9. No enviar nada al comercio en esta fase.

## 4. Contrato de propuesta
Campos mínimos:
- proposal_id único;
- merchant_id y región;
- items con item_id, cantidad explícita y modificadores;
- modalidad y destino solo cuando corresponda;
- subtotal, cargos, descuentos, impuestos y total;
- moneda;
- fuentes y registros de origen;
- retrieved_at y expiración;
- versión del catálogo;
- hash de contenido canónico;
- estado y motivo de abstención, si aplica.

La cantidad debe provenir de la intención o de una regla confirmada. “Pizza para dos personas” no significa dos pizzas. “Dos pizzas” sí expresa cantidad dos. Una intención ambigua no produce propuesta ejecutable.

## 5. Barreras obligatorias
- Denegar por defecto acciones externas.
- Verificar autorización vigente, finalidad y fuente.
- Verificar coincidencia exacta de comercio y región.
- Verificar expiración y versión de propuesta.
- Exigir confirmación humana específica del contenido completo.
- No tratar la confirmación como aceptación del comercio.
- No almacenar credenciales en código, fixtures, logs o repositorio.
- No eludir controles de acceso ni condiciones de uso.
- Rechazar fuentes vencidas, ambiguas o no autorizadas.
- Registrar resultado de cada intento, incluida la abstención.

## 6. Idempotencia para una fase futura
Si se autoriza ejecución en un anexo separado:
- generar una clave idempotente por intención/operación;
- persistirla antes del envío;
- reutilizarla ante reintentos de la misma operación;
- rechazar reutilización con payload diferente;
- conservar identificador externo y respuesta del comercio;
- definir reconciliación cuando el timeout deje resultado incierto;
- nunca reintentar a ciegas una operación cuyo resultado externo sea desconocido.

La idempotencia reduce duplicados técnicos, pero no prueba aceptación ni cumplimiento.

## 7. Estados diferenciados
`DRAFT → VALIDATED → PROPOSED → USER_CONFIRMED` son estados internos de ONECLICK. No significan pedido enviado. En una fase de ejecución futura podrían existir `SUBMITTED`, `MERCHANT_ACCEPTED`, `REJECTED`, `FULFILLED` o `CANCELLED`, pero solo con respuesta/evidencia externa correspondiente.

## 8. Criterios de aceptación de la fase segura
- Consulta únicamente de fuente autorizada.
- Datos vencidos o desconocidos provocan abstención.
- Ninguna ruta de código puede enviar pedidos en READ_ONLY/PROPOSAL.
- Confirmar propuesta no invoca un endpoint externo.
- Propuestas conservan detalle, fuente, vigencia y hash.
- Pruebas cubren duplicados, expiración, comercio/región incorrectos y ambigüedad.
- Logs no exponen credenciales ni datos personales innecesarios.

## 9. Estado real
Este documento define el comportamiento requerido. No afirma que exista un adaptador conectado a un comercio real ni que se hayan probado endpoints productivos. La ejecución permanece DESHABILITADA.
