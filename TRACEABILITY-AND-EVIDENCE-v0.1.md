# CEUNIA / ONECLICK — Trazabilidad y evidencia del piloto
**Versión:** 0.1 · **Estado:** especificación; no acredita eventos comerciales reales

## 1. Objetivo
Definir un registro verificable del ciclo de vida de una prueba: autorización, consulta, propuesta, revisión humana, eventual ejecución autorizada, respuesta externa, comprobante y medición. Los eventos no existentes no se inventan ni se completan retroactivamente.

## 2. Eventos sugeridos
- `AUTHORIZATION_RECORDED`
- `SOURCE_REGISTERED`
- `CATALOG_SNAPSHOT_CREATED`
- `INTENT_RECEIVED`
- `INTERPRETATION_RECORDED`
- `CLARIFICATION_REQUESTED`
- `PROPOSAL_CREATED`
- `PROPOSAL_CONFIRMED_BY_USER`
- `EXECUTION_AUTHORIZED` (solo fase futura)
- `SUBMISSION_ATTEMPTED` (solo fase futura)
- `MERCHANT_RESPONSE_RECEIVED` (solo con respuesta externa)
- `RECEIPT_RECORDED` (solo con comprobante)
- `OUTCOME_VERIFIED`
- `ECONOMIC_MEASUREMENT_RECORDED)
- `AUTHORIZATION_REVOKED`
- `ABSTENTION_RECORDED`

## 3. Sobre de evento
Cada evento debería contener:
- event_id único;
- event_type;
- schema_version;
- occurred_at y recorded_at en ISO-8601 con zona horaria;
- actor_type e identificador seudónimo cuando corresponda;
- merchant_id/pilot_id cuando existan;
- correlation_id y causation_id;
- source_id/source_record_id cuando aplique;
- payload mínimo necesario;
- previous_event_hash y event_hash;
- referencias a evidencia externa, sin copiar secretos.

## 4. Hashes y canonicalización
Calcular SHA-256 sobre una representación canónica documentada del contenido del evento, con codificación UTF-8, orden de claves estable y reglas explícitas para números, fechas y valores nulos. Registrar algoritmo, versión de canonicalización y bytes exactos usados. El hash permite detectar cambios respecto del contenido hasheado; por sí solo no prueba autoría, fecha confiable, identidad ni que el evento haya ocurrido.

Para artefactos externos, conservar referencia, tamaño, tipo MIME, fecha de obtención y SHA-256 del archivo original. No alterar el original. Una corrección genera un nuevo evento que referencia al anterior, nunca una reescritura silenciosa.

## 5. Persistencia SQLite
Esquema lógico mínimo:
- `events(event_id PRIMARY KEY, event_type, occurred_at, recorded_at, correlation_id, payload_json, previous_event_hash, event_hash)`
- `evidence(evidence_id PRIMARY KEY, event_id, uri_or_path, media_type, sha256, captured_at)`
- `authorizations(authorization_id PRIMARY KEY, merchant_id, scope_json, valid_from, valid_until, status, document_hash)`

Aplicar transacciones, restricciones de unicidad, backups protegidos y control de acceso. No guardar contraseñas, tokens ni datos de pago. La retención y el borrado deben definirse antes de usar datos reales.

## 6. Historial y verificación
Una función equivalente a `get_history(pilot_id)` debe devolver eventos ordenados, permitir reconstruir el estado y verificar continuidad de hashes. Debe detectar eventos duplicados, referencias rotas y alteraciones. La disponibilidad de esa función y su cobertura deben verificarse en el código y pruebas antes de declararlas implementadas.

## 7. Separación de entornos
- FIXTURE: datos ficticios, rotulados y no mezclables con producción.
- TEST: datos controlados, sin operaciones comerciales.
- PILOT: solo datos reales autorizados y con controles aprobados.

Cada registro debe identificar ambiente. Los resultados de CI no se presentan como pedidos, ingresos, ahorro ni validación comercial.

## 8. Evidencia de una operación
Para afirmar que un pedido fue enviado se requiere registro del intento y evidencia del canal externo. Para afirmar aceptación se requiere respuesta del comercio. Para afirmar cumplimiento se requiere evidencia de entrega/retiro. Para afirmar pago se requiere comprobante válido. Son estados diferentes.

## 9. Manifiesto de cierre
Al finalizar cada prueba, generar un manifiesto con:
- alcance y versión del protocolo;
- autorización y su hash;
- versiones de código/configuración;
- snapshots y fuentes;
- IDs de eventos y evidencias;
- hashes SHA-256;
- métricas y método;
- excepciones, faltantes y limitaciones;
- responsable de revisión y fecha.

## 10. Estado actual
Esta especificación no confirma que todos estos eventos, tablas, hashes encadenados o `get_history()` estén implementados. Deben verificarse contra el repositorio y CI. No existe aquí evidencia de un comercio autorizado ni de una transacción real.
