# CEUNIA Ω — Inteligencia híbrida evolutiva

**Somos la evolución evolucionando.**  
CEUNIA (Consciencia Evolutiva de Naturaleza Humana e Inteligencia Artificial) propone una arquitectura de inteligencia híbrida para coordinar observación, memoria, simulación, evaluación, decisión, acción y aprendizaje con coherencia y supervisión humana.

## Principio transversal: medición evolutiva

> **CEUNIA mide. Y aprende. Y decide cuándo no activar. Y evoluciona.**

\[
I \rightarrow C \rightarrow D \rightarrow R \rightarrow M \rightarrow A \rightarrow E
\]

**Intención → Comprensión → Decisión → Resolución → Medición → Aprendizaje → Evolución.**

La medición atraviesa toda la arquitectura. Registra tanto las resoluciones como las decisiones de esperar, consultar, solicitar autorización o abstenerse. No activar también puede ser la decisión correcta, siempre que se justifique y pueda revisarse.

### Las tres capas de esta integración

1. **Especificación técnica:** [MEDICION-OMEGA.md](MEDICION-OMEGA.md), con etapas, indicadores, evidencia, registro mínimo y condiciones de no activación.
2. **Síntesis pública:** esta portada del repositorio presenta la ecuación como principio rector de CEUNIA Ω.
3. **Fundamento arquitectónico:** [WHITEPAPER.md](WHITEPAPER.md) incorpora la medición al ciclo evolutivo completo.

## Arquitectura resumida

Estado → Observación → Memoria → Simulación → Evaluación → Punto Albedrío → Decisión → Acción o no activación → Medición → Aprendizaje → Evolución → Estado siguiente.

La metaobservación revisa transversalmente interpretación, decisión, ejecución y medición. La persona conserva el control de las operaciones que requieren consentimiento o autorización.

## Qué es CEUNIA hoy

Una arquitectura y línea de desarrollo documentada, con prototipos y experimentos comunicados por su autor. Cada capacidad debe distinguirse por su nivel de evidencia: concepto, prototipo, prueba controlada, validación externa u operación real. La documentación no afirma que todas las capacidades futuras estén implementadas ni que exista conciencia subjetiva artificial demostrada.

## En qué puede convertirse

En una plataforma modular de inteligencia híbrida que coordine modelos, agentes, memoria y herramientas, y que pueda aplicarse a productos como ONECLICK, manteniendo permisos, trazabilidad, medición y supervisión humana.

## Documentos principales

- [Medición evolutiva Ω](MEDICION-OMEGA.md)
- [White Paper CEUNIA](WHITEPAPER.md)
- [Arquitectura](ARCHITECTURE.md)
- [Métricas](METRICS.md)
- [Productos y ecosistema](PRODUCTS.md)
- [ONECLICK](ONECLICK/README.md)

## Estado y rigor

Las definiciones de esta documentación son una especificación de diseño. Los indicadores deben instrumentarse y validarse con datos adecuados. Los resultados experimentales comunicados por el autor no equivalen a validación independiente. Las publicaciones de GitHub documentan versiones y cambios, pero no sustituyen registros legales de propiedad intelectual.

---
**CEUNIA Ω | En unión y libertad. Co-razón. Co-herencia.**


## Plataforma e integración

- [Arquitectura de plataforma CEUNIA Ω](PLATFORM-ARCHITECTURE.md): orquestación de empresas, modelos de IA, productos, ponderación, consentimiento y despliegue por etapas.
- [Auditoría del Sprint 72 h](AUDITORIA-SPRINT-72H.md): inventario verificado, niveles de evidencia y brechas técnicas.


## Núcleo ejecutable de plataforma (Fase 0)

Se añadieron módulos iniciales y pruebas automatizadas:
- `core/scoring.py`: ponderación precio/tiempo con normalización min-max, pesos configurables, filtros de disponibilidad/autorización y límites duros.
- `core/adapters.py`: contrato de adaptador y adaptador de demostración exclusivamente sandbox.
- `core/consent.py`: puerta explícita de consentimiento, presupuesto e idempotencia.
- `core/orchestrator.py`: comparación de cotizaciones y decisión de abstenerse o solicitar confirmación; no ejecuta compras.
- `tests/test_platform_core.py`: pruebas unitarias.
- `.github/workflows/ceunia-core-tests.yml`: ejecución automática de pruebas en GitHub Actions ante push/PR y manualmente.

**Límite deliberado:** estos módulos no se conectan a PedidosYa, Rappi, Mercado Pago ni otros proveedores reales. Los datos de demostración deben etiquetarse como sandbox y nunca presentarse como cotizaciones reales.


## Demo ejecutable ONECLICK (sandbox)

Desde la raíz del repositorio, con Python 3.11 o compatible:

```bash
python -m unittest discover -s tests -v
python -m examples.oneclick_sandbox
```

La demo recorre intención → adaptadores simulados → cotizaciones → ponderación → decisión. Usa datos ficticios, no llama a comercios ni realiza pedidos o cobros. El workflow de GitHub Actions ejecuta ambas comprobaciones.


## Endurecimiento y verificación continua

El núcleo valida entradas finitas/no negativas, nombres de proveedor, monedas y consistencia de entorno sandbox. Las cotizaciones de distintas monedas fuerzan consulta en lugar de compararse directamente. La moneda se conserva hasta la oferta ordenada. La autorización valida importe, presupuesto, moneda, clave de idempotencia y confirmación explícita.

**CI verificado:** GitHub Actions ejecutó correctamente las pruebas unitarias y la demo ONECLICK sandbox en el commit `909385058c80bc2fcfb6b69682a5e43feb11b64d`. Ejecución: https://github.com/matiasbision-dot/CEUNIA-UNIFIED-SYSTEM/actions/runs/43555022755


## ONECLICK: contrato de pedido y acceso a proveedores

- `core/order_contract.py`: borrador de pedido tipado; exige producto identificado, comercio, región y modalidad. Para entrega exige destino seleccionado. No presupone catálogo ni disponibilidad.
- `assess_order_readiness()`: impide avanzar a cotización si catálogo o disponibilidad del comercio no fueron verificados.
- `ONECLICK-API-ACCESS-MAP.md`: investigación de documentación oficial y límites de acceso de PedidosYa, Rappi y Uber Direct.
- `ONECLICK-PROVIDER-STATUS.md`: estados y límites de evidencia.

**Regla de experiencia:** las preferencias inferidas por el sistema no se convierten en detalles del pedido hasta que el usuario las haya expresado o confirmado. Un borrador listo para cotizar no es una compra ni una cotización real.


### ONECLICK intent layer

- `core/intent.py` extracts a conservative set of explicit Spanish signals (product, quantity, delivery/pickup).
- Ambiguous, conflicting or unknown values remain missing and produce clarification questions; no merchant, variant, address, price or inferred preference is fabricated.
- A complete intent is not automatically a ready order: merchant, catalog, availability, destination and final quote still require verification.
- The execution gateway accepts only `place_order`, requires production evidence and explicit confirmation, and distinguishes accepted, rejected and unknown provider outcomes. Unknown outcomes require reconciliation, never blind retry.


### Runnable intent demo

Run `python -m examples.oneclick_intake` to see the conservative Spanish intake flow. The CI workflow runs this demonstration alongside the sandbox quote comparison.


### ONECLICK prepared-order flow

- `core/oneclick_flow.py` joins explicit Spanish intent, a fresh catalog snapshot, product identity, modifiers, delivery/pickup and budget into a priced order for human review.
- It fails closed on ambiguous intent, stale/unavailable catalog data, product mismatch, missing destination and exceeded budget.
- The output is `READY_FOR_REVIEW`, never a submitted order or payment. No live merchant API is connected by this module.


### ONECLICK review proposal

- `core/proposal.py` creates a deterministic proposal ID from the selected catalog evidence, merchant, product, quantity, modifiers, fulfillment, destination reference, price, currency and validity window.
- `core/oneclick_flow.py` returns this proposal only after explicit intent, catalog freshness, product identity, availability, modifier and budget checks pass.
- The proposal labels its amount as a catalog subtotal, not a guaranteed final checkout total; delivery fees, taxes or other charges must be separately sourced before final confirmation.
- Every proposal requires user confirmation and remains `submitted=False` and `paid=False`. No live merchant API or payment integration is implied.

Run `python -m examples.oneclick_proposal` to inspect a fully assembled review proposal. The fixture is explicitly simulated and is not a live merchant quote. CI runs this demonstration.


### ONECLICK human confirmation boundary

- `core/confirmation.py` records an explicit confirm/decline decision against the exact proposal ID presented to the user and rejects expired proposals.
- A confirmation record is not an order submission, merchant acceptance, stock reservation, payment authorization or payment receipt. Those remain separate steps requiring a verified production provider and durable idempotency controls.
- `examples/oneclick_confirmation.py` demonstrates the boundary with simulated data; CI executes it.


### ONECLICK durable memory (SQLite)

- `core/confirmation_store.py` persists immutable proposal snapshots, one explicit decision per proposal, and sourced outcome events.
- Proposal saves, repeated identical decisions, and repeated outcome events are idempotent. Conflicting decisions or reused event keys with different payloads are rejected.
- The store is a local evidence ledger. It does not submit orders, contact merchants, reserve stock or process payments. Production use requires controlled database access, backups, retention policy and privacy review.
- `examples/oneclick_memory.py` reopens the SQLite database and demonstrates persisted history using simulated data; CI executes it.
