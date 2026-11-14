# CEUNIA Ω | Arquitectura de plataforma

**Versión:** 1.0  
**Estado:** especificación de plataforma; no implica que todas las integraciones estén implementadas.  
**Principio:** CEUNIA no compite con empresas ni modelos de IA. Los coordina como capacidades externas, bajo autorización, evaluación y trazabilidad.

## 1. Propósito

CEUNIA Ω es una capa de inteligencia y orquestación entre personas, organizaciones, productos, modelos de IA y servicios externos. Comprende la intención, selecciona capacidades, pondera alternativas, solicita permisos, coordina la ejecución y mide el resultado.

ONECLICK es la primera experiencia de usuario prioritaria. CEUNIA es el núcleo de coordinación y evaluación. Los proveedores son brazos externos conectados mediante adaptadores autorizados.

## 2. Arquitectura lógica

1. **Experiencia:** botón, texto, voz y canales conversacionales.
2. **Intención y contexto:** interpreta la solicitud, explicita incertidumbre y aplica estándares editables.
3. **Orquestador Ω:** políticas, routing, simulación, riesgo, ponderación y decisión.
4. **Registro de capacidades:** catálogo de proveedores, modelos, herramientas y servicios disponibles por región.
5. **Adaptadores:** contratos independientes para cada API o proveedor.
6. **Control de consentimiento:** permisos, confirmación, presupuesto, límites y revocación.
7. **Ejecución:** estados transaccionales, idempotencia, seguimiento, cancelación cuando sea posible.
8. **Medición y aprendizaje:** resultado, evaluación triple, trazabilidad y mejoras revisables.

Metaobservación y gobernanza atraviesan todas las capas.

## 3. Principio transversal

**Intención → Comprensión → Decisión → Resolución → Medición → Aprendizaje → Evolución.**

La decisión puede ser actuar, esperar, consultar, solicitar autorización o abstenerse. No activar también puede ser la resolución correcta.

## 4. ONECLICK: máxima resolución con mínima expresión

La persona expresa una necesidad con el mínimo de palabras. CEUNIA puede aplicar un estándar predeterminado configurable, pero debe hacerlo visible y editable.

Ejemplo ilustrativo:
- “pizza” puede sugerir mozzarella de 8 porciones;
- “café” puede sugerir café con leche mediano;
- “agua” puede sugerir botella fría de 500 ml.

Los estándares personales se gobiernan por preferencias declaradas y autorizadas. Las estadísticas agregadas pueden sugerir mejoras, nunca modificar silenciosamente una preferencia individual. Una palabra no autoriza por sí sola una compra, un pago ni compartir una ubicación.

## 5. Motor de ponderación

Para alternativas factibles y comparables, el score inicial es:

\[
S_i = w_p P_i^{norm} + w_t T_i^{norm}
\]

Con pesos iniciales equilibrados:

\[
w_p=0.5,\quad w_t=0.5,\quad w_p+w_t=1
\]

Normalización min-max:

\[
P_i^{norm}=\frac{P_i-P_{min}}{P_{max}-P_{min}},\qquad
T_i^{norm}=\frac{T_i-T_{min}}{T_{max}-T_{min}}
\]

Menor score es preferible. Si una dimensión tiene el mismo valor en todas las opciones, su aporte es igual para todas. Antes de ponderar se excluyen opciones no disponibles, no autorizadas o incompatibles con restricciones duras. Se muestran valores absolutos, cargos, calidad, distancia, condiciones y fuente de cotización.

Los pesos son configurables. Precio y tiempo no son siempre las únicas dimensiones; accesibilidad, calidad, confiabilidad y preferencia pueden ser determinantes.

## 6. Potencia fija, dinámica y metapotencia

- **Potencia fija:** infraestructura, conocimiento, modelos, conectores, capacidades y contratos disponibles.
- **Potencia dinámica:** recursos asignados al ciclo actual: presupuesto, tiempo, cómputo, proveedores y contexto.
- **Metapotencia:** observación y ajuste de cómo se distribuyen las potencias fija y dinámica según objetivo, evidencia, riesgo y resultado.

Opera dentro de límites, permisos y presupuestos explícitos. No representa capacidad ilimitada.

## 7. Serendipia institucional

Lo inesperado se evalúa como posible señal. Un error o detalle contextual puede abrir una oportunidad, pero no se presupone que todo error sea valioso.

Proceso: detectar → registrar procedencia → clasificar riesgo/error/oportunidad → generar hipótesis → evaluar → probar de forma segura o solicitar aprobación → medir → conservar aprendizaje verificable.

“Living detail → transformación relevante” es una heurística de descubrimiento.

## 8. Evaluación triple

Cada resolución se analiza en tres planos separados:

1. **Experiencia humana:** satisfacción, esfuerzo, confianza, comprensión y control.
2. **Resultado:** cumplimiento verificable, calidad, tiempo, costo y confiabilidad.
3. **Contexto e impacto:** adecuación situacional, efectos sobre terceros, accesibilidad y consecuencias relevantes.

La satisfacción no sustituye la verificación; la eficiencia no justifica daño contextual.

## 9. Tiempo informacional: hipótesis experimental

La secuencia 3, 6, 9, 15, 24, 39, 63 y su comparación con ventanas binarias 1, 2, 4, 8, 16, 32, 64 se conserva como hipótesis de ventanas temporales. La diferencia 1/64, la “octava continua” y las asociaciones con π, φ o Tesla no se presentan como señal predictiva demostrada.

Para validarla: definir variable objetivo y ventanas antes del test; comparar con baselines simples y ventanas aleatorias; separar entrenamiento, validación y prueba fuera de muestra; corregir comparaciones múltiples; reportar estabilidad, anticipación y falsos positivos, incluidos resultados negativos.

## 10. Integración con empresas y servicios

Categorías previstas: movilidad, comida y comercio, pagos, mensajería, alojamiento, viajes y reservas. Los proveedores se eligen según región y capacidad técnica real.

Cada adaptador debe declarar:
- región y operaciones soportadas;
- documentación y autenticación oficial;
- permisos y datos requeridos;
- tarifas, límites, disponibilidad y términos;
- estados de operación, cancelación y reembolso;
- idempotencia, SLA y tratamiento de errores.

Nombrar una empresa no implica API pública, convenio ni acceso concedido. No se inventan endpoints. Cada integración requiere documentación oficial, credenciales autorizadas, condiciones comerciales y pruebas.

## 11. Integración con modelos de IA

Los modelos son capacidades intercambiables para lenguaje, voz, visión, búsqueda, planificación o evaluación. CEUNIA conserva el control del flujo, los permisos, la política de memoria, la medición y el registro.

Cada proveedor requiere endpoint oficial, credenciales y alcance permitido. Solo se envía la información mínima necesaria. No se presupone acceso a Meta AI/Muse, OpenAI, Anthropic, Google, Perplexity o ElevenLabs por el hecho de mencionarlos.

## 12. Seguridad y transacciones

- Secretos fuera del repositorio, mediante variables de entorno o gestor de secretos.
- Ninguna compra, reserva, viaje, pago o acción irreversible sin confirmación explícita.
- Mostrar proveedor, importe total, cargos, condiciones, dirección y tiempo estimado antes de confirmar.
- Idempotencia para prevenir duplicados.
- Estados transaccionales y referencias de proveedor para seguimiento.
- Consentimiento revocable, minimización de datos y registros protegidos.
- Cancelación, devolución y soporte según capacidades del proveedor.

## 13. Despliegue por etapas

**Fase 0 — Núcleo demostrable:** pruebas automatizadas, motor de ponderación, contratos de adaptadores, catálogo de estándares y simulador con datos claramente identificados como ficticios o sandbox.

**Fase 1 — Piloto local:** un caso de uso, un proveedor con acceso real y un medio de pago autorizado. Si no hay API disponible, piloto asistido sin simular una integración automática.

**Fase 2 — Multi-proveedor:** comparación entre proveedores activos y equivalentes de una categoría.

**Fase 3 — Plataforma multi-vertical:** movilidad, comercio, alojamiento, viajes y otros dominios, con gobernanza, observabilidad y evaluación continua.

## 14. Criterio de madurez

Una integración se considera operativa solo cuando existen documentación oficial, acceso autorizado, pruebas de contrato, prueba de extremo a extremo, confirmación de usuario, registro de resultado y manejo de errores. La documentación arquitectónica no equivale a integración desplegada.
