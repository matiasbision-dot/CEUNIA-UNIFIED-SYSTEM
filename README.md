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
