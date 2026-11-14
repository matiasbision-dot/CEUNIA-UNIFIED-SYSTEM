# ONECLICK — Paquete de incorporación del primer comercio

**Versión:** 0.1  
**Estado:** PLANTILLA PREPARADA / SIN COMERCIO SELECCIONADO  
**Ámbito inicial:** una pizzería independiente de Mar del Plata, Argentina  
**Modo inicial:** consulta y propuesta; ejecución externa deshabilitada  
**Dependencia de activación:** autorización escrita del comercio y validación técnica de su fuente

> Este documento prepara la incorporación. No constituye un acuerdo firmado, autorización vigente, integración productiva ni evidencia de una operación comercial.

## 1. Objetivo y límites

Incorporar un único comercio para probar si ONECLICK convierte una intención humana explícita en una propuesta correcta, vigente, trazable y útil, y eventualmente en una operación real autorizada.

La primera etapa se limita a:
- consultar un catálogo y disponibilidad que el comercio haya autorizado;
- identificar procedencia, fecha de observación, vigencia y condiciones;
- interpretar una intención sin inventar cantidades ni preferencias;
- presentar una propuesta con total comparable y modalidad de entrega/retiro;
- solicitar revisión y confirmación humana;
- mantener deshabilitado el envío externo hasta superar las puertas de autorización y producción.

Fuera de alcance por defecto: cobro, almacenamiento de tarjetas, marketing, perfilado, reventa de datos, publicación del catálogo, pedidos automáticos, acceso a sistemas no autorizados y uso de datos para finalidades distintas.

## 2. Acuerdo de autorización y finalidad de datos

**Plantilla para completar y revisar con las partes. No firmar con campos vacíos. Requiere revisión legal local antes de su uso vinculante.**

### Partes
- Comercio / razón social: [COMPLETAR]
- CUIT: [COMPLETAR]
- Domicilio comercial: [COMPLETAR]
- Representante y facultades: [COMPLETAR]
- Responsable de ONECLICK: [COMPLETAR]
- Fecha de inicio y vencimiento: [COMPLETAR]
- Contacto para revocación/incidentes: [COMPLETAR]

### Autorización específica
El comercio autoriza a ONECLICK, durante la vigencia indicada, a acceder únicamente a:
- [ ] catálogo de productos y variantes;
- [ ] precios y moneda;
- [ ] disponibilidad y horarios;
- [ ] zonas, costos y condiciones de entrega;
- [ ] condiciones de retiro;
- [ ] estado de una operación iniciada con autorización expresa;
- [ ] comprobante o referencia de resultado estrictamente necesaria para reconciliar la prueba.

**Fuente/canal autorizado:** [API / archivo / panel / otro: COMPLETAR]  
**Identidad del titular de la fuente y permiso:** [COMPLETAR]  
**Finalidad única:** preparar y, si se habilita por separado, tramitar propuestas/pedidos solicitados expresamente por el usuario y medir el resultado de la prueba.  
**Región/localidad:** [COMPLETAR]  
**Usuarios/datos personales incluidos:** minimizar; no incorporar datos de clientes del comercio salvo necesidad demostrada, base válida y autorización específica.  
**Retención:** [PLAZO Y JUSTIFICACIÓN]  
**Subencargados/servicios técnicos:** [COMPLETAR O “NINGUNO”]  
**Exportación, redistribución o publicación:** no autorizadas salvo anexo explícito.  
**Contraprestación/distribución de valor:** no definida hasta acuerdo separado firmado; no se presume comisión ni porcentaje.

### Condiciones de control
1. El permiso se limita a la finalidad, campos, fuente, región y plazo expresamente indicados.
2. El comercio declara tener facultades para conceder el acceso y que el canal indicado permite el uso propuesto.
3. ONECLICK no altera precios, disponibilidad ni condiciones del comercio.
4. El comercio puede suspender el acceso o revocar la autorización mediante el contacto indicado. La revocación detiene nuevas consultas y ejecuciones; se preservan únicamente los registros que deban conservarse por obligación legal o para demostrar una operación ya realizada.
5. Incidentes, errores de catálogo o discrepancias se notifican a [CONTACTO / PLAZO].
6. Cualquier finalidad, campo, integración, región o modalidad nueva exige autorización adicional.
7. La autorización para consultar datos no autoriza a enviar pedidos, cobrar, cancelar ni modificar operaciones.

### Habilitación separada de ejecución
La ejecución externa requiere un anexo independiente que especifique: endpoint/canal, operaciones permitidas, límites, credenciales bajo custodia segura, política de cancelación, idempotencia, conciliación, responsables y evidencia de aceptación. Hasta entonces: **NO ACTIVAR ENVÍO**.

**Firmas:**  
Comercio: ____________________ Fecha: __________  
ONECLICK: ____________________ Fecha: __________

## 3. Ficha de catálogo y vigencia

Un registro por producto/variante. No cargar precios estimados como si fueran precios del comercio.

| Campo | Tipo / regla |
|---|---|
| merchant_id | identificador estable del comercio |
| product_id | identificador estable del producto |
| variant_id | identificador de variante; nullable si no aplica |
| name | nombre exacto publicado por el comercio |
| description | descripción provista por la fuente |
| category | categoría |
| price_amount | decimal exacto, nunca float binario |
| currency | código de moneda acordado, p. ej. ARS |
| tax_included | true / false / unknown |
| availability_status | available / unavailable / limited / unknown |
| modifiers | opciones permitidas, con precio y límites |
| fulfillment_modes | pickup / delivery, solo los habilitados |
| delivery_fee | decimal + moneda + zona + condiciones; nullable si no aplica |
| minimum_order | decimal + moneda; nullable si no aplica |
| observed_at | timestamp ISO 8601 con zona |
| valid_until | vencimiento explícito o política de vigencia |
| source_id | fuente autorizada |
| source_record_id | identidad del registro de origen |
| permission_ref | referencia al acuerdo/autorización vigente |
| content_hash | SHA-256 del contenido canónico del registro |
| status | active / expired / withdrawn / rejected |

Reglas:
- Montos decimales y moneda explícita; no inferir impuestos, recargos ni envío.
- Disponibilidad desconocida no equivale a disponible.
- Si no hay valid_until, aplicar una ventana de frescura aprobada por el comercio; si vence, abstenerse y solicitar actualización.
- Conservar la fuente y el instante de observación. Un precio copiado sin procedencia no es dato vivo verificable.
- Los modificadores deben tener reglas y precios claros; no inventar combinaciones.
- La suma final debe reflejar productos, modificadores, descuentos, impuestos, envío y cargos aplicables.

## 4. Adaptador del comercio: contrato de seguridad

### Modos
- **DISABLED:** sin acceso externo.
- **READ_ONLY:** consulta únicamente a la fuente autorizada.
- **PROPOSAL_ONLY:** genera propuestas; no transmite pedidos.
- **PRODUCTION_GATED:** solo después de verificar autorización de ejecución, capacidad productiva, credenciales, idempotencia, ledger y pruebas de extremo a extremo.

Estado inicial obligatorio: **READ_ONLY o DISABLED**. El paso a PRODUCTION_GATED no es automático.

### Requisitos antes de cualquier envío
- autorización de ejecución vigente y verificable;
- comercio, región, operación y canal coincidentes con el permiso;
- propuesta exacta, no vencida y revisada por el usuario;
- confirmación humana explícita para esa propuesta concreta;
- importe final, moneda, modalidad y destino revisados;
- adaptador identificado como productivo y probado;
- clave de idempotencia estable por operación;
- reserva atómica en ledger persistente;
- política de timeout y reconciliación;
- recibo externo verificable y coincidente con comercio y clave.

Si falta una condición, la respuesta es denegar o abstenerse. No reintentar a ciegas ante timeout. Marcar RECONCILIATION_REQUIRED hasta consultar el estado externo por un canal autorizado.

### Estados de una operación
INTENT_RECEIVED → CLARIFICATION_REQUIRED | PROPOSAL_READY → USER_REVIEWED → USER_CONFIRMED → SUBMISSION_AUTHORIZED → SUBMITTED → MERCHANT_ACCEPTED | MERCHANT_REJECTED | RECONCILIATION_REQUIRED → RECEIPT_VERIFIED → OUTCOME_RECORDED

Los estados no son intercambiables:
- propuesta no significa confirmación;
- confirmación del usuario no significa envío;
- envío no significa aceptación;
- aceptación no significa pago;
- pago no significa entrega;
- una pantalla local no es un comprobante del comercio.

## 5. Protocolo de prueba

### Fase A — preparación sin operación
1. Verificar identidad y facultades del comercio.
2. Revisar autorización, finalidad, campos, vigencia y revocación.
3. Registrar la fuente y el canal permitido.
4. Importar una muestra controlada del catálogo.
5. Validar decimales, moneda, disponibilidad, zonas, retiro y delivery.
6. Ejecutar pruebas de datos vencidos, ausentes, contradictorios y no autorizados.
7. Confirmar que el adaptador no puede enviar pedidos.

### Fase B — prueba de propuesta
1. Definir una intención concreta y un baseline comparable.
2. Capturar inicio de medición.
3. Interpretar cantidad, productos, variantes y modalidad.
4. Preguntar ante cualquier ambigüedad material.
5. Consultar solo la fuente autorizada.
6. Verificar procedencia, permiso, calidad y vigencia.
7. Calcular total comparable.
8. Mostrar propuesta y condiciones al usuario.
9. Registrar aceptación/rechazo de la propuesta, sin confundirlo con una compra.

### Fase C — operación real (bloqueada hasta anexo)
1. Confirmar el anexo de ejecución y las pruebas de producción.
2. Mostrar el pedido exacto y el total final.
3. Recibir autorización explícita del usuario para esa operación.
4. Enviar una sola vez con idempotencia.
5. Obtener estado y recibo del comercio.
6. Conciliar la respuesta; ante incertidumbre, no duplicar.
7. Registrar el resultado real y cerrar medición.

### Casos negativos obligatorios
- “pizza para dos” no debe convertirse automáticamente en dos pizzas;
- “dos pizzas” representa cantidad dos;
- “pizza y sushi” exige aclaración si el alcance no es inequívoco;
- “sin delivery” y “delivery y retiro” requieren resolver modalidad;
- “para retirar” nunca se transforma silenciosamente en delivery;
- precio vencido, disponibilidad desconocida o permiso revocado bloquean la propuesta;
- timeout después de enviar no habilita un segundo envío automático;
- falta de recibo verificable mantiene el resultado como no reconciliado.

## 6. Comprobante y medición económica

Cada prueba debe vincular intención, baseline, propuesta, fuente, autorización, decisión y resultado mediante identificadores estables.

### Cinco dimensiones
1. **Tiempo ahorrado:** segundos baseline menos segundos ONECLICK, con inicio/fin definidos.
2. **Errores evitados:** errores baseline menos errores ONECLICK, con taxonomía común.
3. **Mejora de precio/resultado:** total comparable baseline menos total ONECLICK en la misma moneda; incluir cargos, envío, descuentos e impuestos aplicables.
4. **Contribución de fuente:** source_id, source_record_id y evidencia de la contribución efectiva. Consultar una fuente no basta.
5. **Distribución de valor:** no definida / términos autorizados / reconciliada, con referencia a términos firmados. No presumir porcentajes ni pagos.

Sin baseline comparable, resultado verificable o recibo, declarar la métrica como no medida/no verificada. No monetizar tiempo o errores sin método de valoración aprobado.

### Campos mínimos del comprobante de prueba
- trial_id, intent_id, proposal_id, merchant_id;
- timestamps y zona horaria;
- baseline y método de comparación;
- líneas del pedido, cantidades y modificadores;
- modalidad y zona;
- total, moneda y componentes del precio;
- fuente, registro, observed_at, valid_until y permiso;
- confirmación del usuario y su alcance;
- idempotency_key si hubo envío;
- estado externo, receipt_ref y evidencia de conciliación;
- métricas calculadas y estado de verificación;
- hash del evento y referencia al evento anterior.

El comprobante de prueba no sustituye factura, ticket fiscal ni comprobante de pago del comercio.

## 7. Registro trazable y SHA-256

Mantener un registro append-only de eventos. SQLite puede servir para el prototipo local; antes de producción hacen falta controles de acceso, cifrado, copias de seguridad, retención, recuperación, monitoreo y pruebas operativas.

### Eventos sugeridos
INTENT_CAPTURED, SOURCE_AUTHORIZED, CATALOG_OBSERVED, PROPOSAL_CREATED, PROPOSAL_REVIEWED, USER_CONFIRMED, SUBMISSION_AUTHORIZED, ORDER_SUBMITTED, MERCHANT_RESPONSE, RECEIPT_VERIFIED, OUTCOME_RECORDED, PERMISSION_REVOKED, RECONCILIATION_REQUIRED.

### Sobre los hashes
- Serializar cada evento de forma canónica y determinista (UTF-8, claves ordenadas, formato decimal/timestamp definido).
- Calcular SHA-256 del contenido canónico y guardar algoritmo, versión de esquema y hash.
- Encadenar cada evento con el hash del evento anterior para detectar alteraciones dentro de la cadena.
- Un hash acredita integridad respecto del contenido hasheado; por sí solo no acredita autoría, fecha cierta, consentimiento, veracidad del dato ni existencia de una operación.
- Para reforzar evidencia, conservar originales de fuente, recibos y autorizaciones con control de acceso y marcas de tiempo confiables.
- No incluir contraseñas, tokens, datos de tarjetas ni secretos en eventos o hashes.
- get_history() debe devolver eventos ordenados y verificables, sin modificar el registro. Toda corrección se agrega como nuevo evento, nunca sobrescribiendo el anterior.

## 8. Puertas de aceptación del piloto

| Puerta | Evidencia requerida | Estado inicial |
|---|---|---|
| Identidad y facultades | datos y representación verificados | PENDIENTE |
| Autorización de consulta | acuerdo firmado y fuente identificada | PENDIENTE |
| Catálogo | muestra real, procedencia y vigencia | PENDIENTE |
| Propuesta | casos positivos y negativos aprobados | PENDIENTE |
| Medición | baseline y taxonomía documentados | PENDIENTE |
| Ejecución | anexo firmado y canal productivo verificado | BLOQUEADA |
| Resultado | respuesta y recibo verificables | PENDIENTE |
| Economía | cinco dimensiones reportadas sin inferencias | PENDIENTE |

**No declarar piloto productivo ni valor económico demostrado hasta que las puertas correspondientes tengan evidencia.**

## 9. Estado del paquete

Preparado como plantilla reutilizable. No hay comercio elegido, acuerdo firmado, fuente real autorizada, catálogo real conectado ni pedido enviado. La integración productiva permanece deshabilitada.

**Principio rector:** máxima resolución, mínima expresión; datos mínimos, finalidad explícita, procedencia verificable, control humano y resultado medido.
