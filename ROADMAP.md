# CEUNIA Ω — Roadmap de plataforma

## Estado actual · Sprint de resultados 72 horas

La base documental pública está consolidada. Existe un MVP Python modular y un prototipo de interfaz ONECLICK. La auditoría de repositorio distingue con precisión código existente, especificaciones y capacidades todavía no verificadas.

**Día 1 — Consolidación: completado documentalmente**
- [Auditoría de estado y brechas](AUDITORIA-SPRINT-72H.md)
- [Arquitectura de plataforma](PLATFORM-ARCHITECTURE.md)
- [Medición evolutiva Ω](MEDICION-OMEGA.md)
- README y White Paper con medición evolutiva integrada.

**Día 2 — Construcción**
- pruebas automatizadas reproducibles para el núcleo;
- motor de ponderación precio/tiempo con normalización y casos límite;
- contratos de adaptadores y simulador de proveedores;
- control de consentimiento, no activación y registro de eventos;
- especificación API y persistencia segura.

**Día 3 — Demostración y evidencia**
- ejecutar y documentar pruebas;
- verificar despliegue y comportamiento de ONECLICK;
- preparar una demo de extremo a extremo sin simular integraciones reales;
- cerrar inventario de capacidades, limitaciones y próximos pasos comerciales.

## Fases de plataforma

### Fase 0 — Núcleo demostrable
Pruebas, ponderación, catálogo de capacidades, contratos de adaptadores, simulación y trazabilidad.

### Fase 1 — Piloto local
Un único flujo de usuario y un proveedor con API o acceso autorizado. Un medio de pago solo después de revisar documentación, condiciones y permisos. Si no hay integración, piloto asistido, claramente identificado como tal.

### Fase 2 — Multi-proveedor
Comparación de proveedores equivalentes activos, con disponibilidad, precio total, tiempo, calidad y condiciones verificadas.

### Fase 3 — Plataforma multi-vertical
Movilidad, comercio, pagos, alojamiento, viajes y mensajería, mediante adaptadores independientes.

### Fase 4 — Inteligencia híbrida
Selección de modelos y herramientas por tarea, memoria gobernada, evaluación, metaobservación y aprendizaje versionado.

### Fase 5 — Tiempo informacional y predicción
Evaluación experimental de hipótesis temporales y patrones predictivos, con baselines, pruebas fuera de muestra y publicación de resultados negativos.

## Criterio de avance

Una fase se cierra solo con artefacto verificable, pruebas y límites documentados. Una propuesta no se presenta como implementación; una implementación no se presenta como validación; un resultado experimental no se presenta como validación externa.

---
**Principio rector:** CEUNIA mide. Aprende. Decide cuándo no activar. Evoluciona.
