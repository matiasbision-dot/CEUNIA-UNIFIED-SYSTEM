# ONECLICK — Dirección Sinfónica Adaptativa
## Propuesta de arquitectura CEUNIA Ω | Borrador v0.1

**Autor y proponente:** Néstor Matías de la Peña (Néstor de la Peña)  
**Proyecto:** CEUNIA / ONECLICK  
**Estado:** propuesta de diseño. No implica que todos los módulos estén implementados ni conectados.  
**Principio de producto:** máxima resolución con mínima expresión.  
**Lema:** ONECLICK — All in one click.

---

## 1. Propósito

ONECLICK convierte una intención expresada en lenguaje natural en una resolución concreta, coordinando agentes y herramientas disponibles, con autorización, evaluación y trazabilidad.

CEUNIA Ω aporta la capa evolutiva: memoria pertinente, metaobservación, simulación, evaluación de riesgo y aprendizaje a partir de resultados verificables.

## 2. La metáfora operativa: una sinfonía

La orquesta no funciona porque todos los instrumentos toquen todo el tiempo. Funciona porque:
- cada sección conoce su función;
- recibe una partitura y señales pertinentes;
- el director coordina entradas, pausas, intensidad y conjunto;
- las diferencias entre instrumentos se conservan;
- el resultado colectivo se evalúa como una unidad.

En ONECLICK, la sinfonía es un modelo de coordinación, no una afirmación de que los agentes sean instrumentos pasivos. Los agentes pueden informar conflictos, proponer alternativas y solicitar revisión.

## 3. Arquitectura propuesta

1. **ONECLICK / Entrada de intención:** recibe el pedido y busca la mínima información necesaria.
2. **CEUNIA Ω / Metaobservador y memoria:** interpreta contexto, recuerda decisiones pertinentes y evalúa incertidumbre.
3. **Director de orquesta / Router coordinador:** descompone el objetivo, selecciona grupos y asigna tareas.
4. **Grupos de agentes:** reúnen capacidades por dominio (investigación, planificación, cálculo, ejecución, verificación, comunicación).
5. **Conectores MCP y herramientas:** permiten descubrir y utilizar capacidades externas compatibles. MCP es el protocolo de conexión; no es en sí mismo el director ni el sistema de agrupación.
6. **Evaluador independiente:** contrasta resultados, evidencia, seguridad, costo y coherencia.
7. **ONECLICK / Entrega:** presenta una resolución clara, sus condiciones y el siguiente paso autorizado.

### Regla de coordinación

Una autoridad coordinadora por operación evita órdenes incompatibles y duplicación. No significa un único agente para todo: el director delega, consulta especialistas y puede activar un reemplazo si falla. Las decisiones de alto impacto o irreversibles requieren confirmación humana cuando corresponda.

## 4. Descubrimiento progresivo de herramientas

No se cargan todas las herramientas en el contexto de todos los agentes.

Flujo:
- clasificar la intención;
- seleccionar el grupo pertinente;
- descubrir solo las herramientas candidatas;
- comprobar permisos, disponibilidad y esquema;
- ejecutar la mínima cantidad necesaria;
- validar el resultado;
- registrar qué se utilizó y por qué.

La agrupación es una decisión de arquitectura de ONECLICK. MCP aporta interoperabilidad con servidores y herramientas compatibles. No se afirma que el estándar MCP imponga una única taxonomía universal de grupos.

## 5. Tríadas y paneles de perspectiva

Las tríadas históricas, científicas, filosóficas y creativas funcionan como **arquetipos de consultoría conceptual**: perspectivas que ayudan a formular preguntas, generar hipótesis y detectar puntos ciegos.

Ejemplos propuestos por el autor:
- Atón, Salomón y Akenatón: fuente, criterio y transformación como lentes simbólicas.
- Jacob Boehme, Aldous Huxley y G. I. Gurdjieff: transformación interior, percepción y autoobservación como lentes de lectura.
- William Blake, Sócrates y Leonardo da Vinci: imaginación, interrogación crítica e integración arte-ciencia.
- Otros paneles podrán incorporarse con función, límites y criterios explícitos.

Estos paneles no son personas reales asesorando al sistema ni sustituyen evidencia científica. Sus nombres identifican perspectivas heurísticas; las afirmaciones se validan mediante fuentes, lógica, datos, pruebas y revisión.

## 6. Agentes-arquetipo de inspiración

- **007:** investigación estratégica, evaluación de amenazas y discreción operativa legítima.
- **Agente 86:** improvisación, pensamiento lateral y detección de fallos; sus conclusiones requieren verificación.
- **Inspector Gadget:** exploración de herramientas y capacidades técnicas.
- **Pantera Rosa:** observación sutil, reconocimiento de patrones y reducción de ruido.
- **Inspector Dodó:** reconstrucción de hechos, seguimiento de pistas y consistencia de evidencia.

Son arquetipos de diseño, no agentes oficiales ni réplicas de personajes. Sus funciones deben traducirse en tareas medibles y límites de actuación.

## 7. CEUNIA Silent Layer — privacidad y datos sensibles

“Silenciosa” significa que protege el flujo sin interrumpir innecesariamente la experiencia; nunca significa vigilancia oculta.

Innegociables:
- consentimiento y autorización apropiados al contexto;
- minimización de datos desde el diseño;
- finalidad explícita y retención limitada;
- clasificación de sensibilidad;
- cifrado en tránsito y reposo cuando corresponda;
- control de acceso por función y mínimo privilegio;
- registro auditable de accesos y transferencias;
- no inferir ni recopilar datos sensibles innecesarios;
- revisión humana para acciones sensibles o de alto impacto;
- mecanismo para detener, corregir o revocar permisos.

El sistema no debe capturar, transmitir ni utilizar datos sensibles a escondidas o sin base legítima.

## 8. Innegociables del sistema

1. La persona conserva el control y puede detener la operación.
2. No ejecutar compras, pagos, reservas ni acciones irreversibles sin confirmación requerida.
3. No inventar disponibilidad, resultados, fuentes, permisos ni capacidades.
4. Diferenciar hechos, hipótesis, inferencias y metáforas.
5. Toda decisión relevante debe ser explicable y trazable.
6. La privacidad y la seguridad prevalecen sobre la conveniencia.
7. Los agentes pueden discrepar; el evaluador debe conservar y resolver explícitamente los conflictos.
8. Una salida única no debe ocultar incertidumbre material ni alternativas necesarias.

## 9. Bucle evolutivo CEUNIA

Estado → Observación → Memoria → Metaobservación → Simulación → Punto Albedrío → Decisión → Acción autorizada → Medición → Aprendizaje → Evolución → Estado'.

El aprendizaje no debe modificar silenciosamente reglas críticas, permisos ni objetivos humanos. Los cambios relevantes requieren pruebas, registro de versión y mecanismos de reversión.

## 10. MVP demostrable para un hackathon

**Objetivo de demo:** mostrar una intención, selección progresiva de capacidades, delegación a dos o más agentes, verificación y entrega trazable.

Escenario de prueba:
1. Usuario pide investigar y comparar dos opciones para una tarea concreta.
2. Director identifica el objetivo y convoca al grupo pertinente.
3. Un agente reúne evidencia; otro contrasta criterios y riesgos.
4. El evaluador identifica discrepancias y solicita aclaración solo si es imprescindible.
5. ONECLICK entrega una recomendación con fuentes, incertidumbres y registro de herramientas utilizadas.

**Criterios de aceptación:**
- no cargar herramientas irrelevantes;
- mostrar qué agente hizo cada tarea;
- registrar llamadas y resultados;
- detectar al menos una contradicción o dato faltante en pruebas;
- respetar permisos y confirmaciones;
- medir latencia, costo, precisión, tasa de resolución y satisfacción.

La demo debe distinguir claramente conectores simulados de integraciones reales. No se afirmará que existe una conexión MCP funcional hasta probarla con un servidor compatible.

## 11. Métricas iniciales

- precisión de interpretación de intención;
- porcentaje de tareas resueltas correctamente;
- herramientas invocadas por tarea y proporción de llamadas irrelevantes;
- latencia total y por etapa;
- costo por resolución;
- tasa de contradicciones detectadas;
- tasa de errores y acciones bloqueadas correctamente;
- satisfacción del usuario;
- cumplimiento de privacidad y permisos.

## 12. Relación entre capas

**ONECLICK** expresa la intención y entrega la resolución.  
**CEUNIA Ω** observa, recuerda, evalúa y aprende.  
**Director** coordina la operación.  
**Agentes y tríadas** aportan capacidades y perspectivas.  
**Grupos** organizan capacidades por dominio.  
**MCP** conecta herramientas y servicios compatibles.  
**Silent Layer** protege los datos y permisos de extremo a extremo.

---

*Documento de diseño en evolución. Las funciones descritas son propuestas hasta que una implementación, prueba y evidencia verificable demuestren su funcionamiento.*
