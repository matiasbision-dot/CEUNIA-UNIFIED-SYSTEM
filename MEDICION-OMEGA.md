# CEUNIA Ω | MEDICIÓN EVOLUTIVA

**Documento:** MEDICION-OMEGA.md  
**Versión:** 1.0  
**Estado:** especificación conceptual y operativa inicial; las métricas requieren instrumentación y validación antes de considerarse resultados demostrados.  
**Ámbito:** principio transversal de CEUNIA Ω. No es un módulo aislado.

## 1. Principio rector

> **CEUNIA mide. Y aprende. Y decide cuándo no activar. Y evoluciona.**

La medición evolutiva acompaña todo el ciclo de CEUNIA: desde la intención inicial hasta el resultado observado y la actualización del estado del sistema. No evalúa solamente si una acción produjo una respuesta; también evalúa si correspondía actuar, esperar, consultar, pedir autorización o abstenerse.

## 2. Ecuación de evolución

\[
I \rightarrow C \rightarrow D \rightarrow R \rightarrow M \rightarrow A \rightarrow E
\]

**Intención → Comprensión → Decisión → Resolución → Medición → Aprendizaje → Evolución.**

| Símbolo | Etapa | Pregunta de control | Evidencia mínima |
|---|---|---|---|
| I | Intención | ¿Qué necesita lograr la persona? | Solicitud original y contexto autorizado |
| C | Comprensión | ¿Qué interpretó el sistema y con qué confianza? | Interpretación, supuestos y ambigüedades |
| D | Decisión | ¿Actuar, esperar, consultar o abstenerse? | Alternativas evaluadas, regla y motivo |
| R | Resolución | ¿Qué respuesta o acción se produjo? | Resultado, estado y responsable |
| M | Medición | ¿Qué ocurrió realmente frente al objetivo? | Métrica, evidencia, desviación y límites |
| A | Aprendizaje | ¿Qué debe conservarse o corregirse? | Retroalimentación y cambio propuesto |
| E | Evolución | ¿Qué cambió en el siguiente estado? | Versión, parámetro o procedimiento actualizado |

La metaobservación es transversal: puede revisar la interpretación, la decisión, la ejecución y la medición. No sustituye la supervisión humana ni convierte una inferencia en un hecho.

## 3. No activar también es una decisión

CEUNIA debe distinguir y registrar, como mínimo, estos resultados de control:

- **ACTUAR:** existe comprensión suficiente, autorización válida y condiciones adecuadas.
- **ESPERAR:** falta una condición temporal o una señal necesaria.
- **CONSULTAR:** existe ambigüedad relevante o falta información.
- **SOLICITAR AUTORIZACIÓN:** la operación requiere consentimiento explícito.
- **ABSTENERSE / NO ACTIVAR:** el riesgo, la incertidumbre, la falta de permiso o la incoherencia superan los límites aceptables.

Una no activación no es un fallo por defecto. Puede ser la resolución correcta. Debe quedar registrada con motivo, contexto, regla aplicada y condición que permitiría reconsiderarla. No se deben ejecutar acciones de alto impacto o irreversibles sin autorización expresa y controles apropiados.

## 4. Dimensiones de medición

Cada ciclo puede evaluarse en estas dimensiones:

1. **Fidelidad de intención:** correspondencia entre lo pedido y lo comprendido.
2. **Calidad de comprensión:** precisión, cobertura de contexto y reconocimiento de incertidumbre.
3. **Idoneidad de decisión:** adecuación entre alternativas, reglas, riesgos y permisos.
4. **Calidad de resolución:** cumplimiento del objetivo y utilidad para la persona.
5. **Eficiencia:** tiempo, pasos, recursos y costo, sin sacrificar seguridad.
6. **Coherencia:** alineación entre intención, contexto, memoria, decisión y resultado.
7. **Seguridad y autonomía:** respeto de privacidad, consentimiento, límites y control humano.
8. **Aprendizaje verificable:** mejora observada en pruebas comparables, no mera modificación del sistema.
9. **Trazabilidad:** posibilidad de reconstruir qué se sabía, qué se decidió y qué sucedió.

## 5. Indicadores iniciales

Los indicadores se definen antes de medir. No deben publicarse puntuaciones sin especificar denominador, conjunto de casos, ventana temporal, método y evidencia.

| Indicador | Definición inicial |
|---|---|
| Tasa de comprensión correcta | Casos cuya interpretación fue validada / casos evaluados |
| Tasa de resolución efectiva | Objetivos completados y verificados / objetivos aceptados |
| Tasa de corrección humana | Casos en que la revisión humana corrigió una inferencia o decisión / casos revisados |
| Tasa de no activación adecuada | Abstenciones justificadas y posteriormente validadas / abstenciones revisadas |
| Tasa de activación indebida | Acciones iniciadas sin condiciones o permisos suficientes / acciones iniciadas |
| Tiempo de resolución | Tiempo entre recepción de intención y resultado verificable |
| Costo por resolución | Recursos y costos atribuibles / resoluciones verificadas |
| Tasa de recurrencia del error | Errores repetidos tras una corrección / oportunidades comparables |
| Cobertura de trazabilidad | Ciclos con registro completo / ciclos medidos |

Las métricas deben desagregarse por tipo de tarea y nivel de riesgo. Una mejora agregada no debe ocultar deterioros en casos críticos.

## 6. Registro mínimo por ciclo

Cada ciclo debe poder generar un registro estructurado con:

- identificador del ciclo y versión del sistema;
- fecha y hora, con zona horaria;
- intención original y contexto estrictamente necesario;
- interpretación del sistema, supuestos e incertidumbre;
- alternativas consideradas;
- decisión: actuar, esperar, consultar, solicitar autorización o abstenerse;
- motivo de la decisión y regla aplicada;
- permisos y confirmaciones recibidos, sin almacenar secretos;
- acción ejecutada o razón de no ejecución;
- resultado observado y evidencia disponible;
- métricas calculadas y método de cálculo;
- revisión humana, correcciones y desacuerdos;
- aprendizaje propuesto y estado de aprobación;
- cambios posteriores, responsable y referencia de versión.

Los registros deben minimizar datos personales, aplicar controles de acceso y respetar plazos de conservación. Un hash o registro externo puede ayudar a detectar alteraciones, pero no demuestra por sí solo que el contenido original fuera verdadero.

## 7. Condiciones de aprendizaje y evolución

Un ciclo no autoriza automáticamente un cambio permanente. Para convertir observaciones en aprendizaje operativo:

1. separar hechos observados de inferencias;
2. comprobar la calidad y representatividad de la evidencia;
3. comparar con una línea de base;
4. evaluar efectos adversos y regresiones;
5. solicitar revisión humana cuando el cambio afecte permisos, seguridad o decisiones relevantes;
6. versionar el cambio y conservar la posibilidad de reversión;
7. medir nuevamente en condiciones comparables.

**Aprender no es simplemente recordar. Evolucionar no es simplemente cambiar.** El cambio debe demostrar una mejora relevante sin degradar dimensiones críticas.

## 8. Relación con los motores CEUNIA Ω

La medición atraviesa Memoria, Router, Simulación, Evaluador, Metaobservador y Aprendizaje. Cada motor aporta evidencia; ninguno puede declararse correcto únicamente por su propia puntuación.

- **Memoria:** conserva contexto pertinente, procedencia y correcciones autorizadas.
- **Router:** registra por qué eligió una ruta, modelo o recurso.
- **Simulación:** compara alternativas y explicita supuestos.
- **Evaluador:** contrasta resultados con criterios definidos.
- **Metaobservador:** revisa coherencia, incertidumbre y posibles errores de evaluación.
- **Aprendizaje:** propone cambios verificables y versionados.

## 9. Gobernanza y límites

- La persona mantiene el control de las decisiones que requieren su autorización.
- La confianza del modelo no equivale a evidencia externa.
- Los resultados informados por el autor deben identificarse como tales hasta que exista reproducción independiente.
- Las métricas exploratorias no son leyes universales ni garantías de rendimiento.
- La medición no debe incentivar acciones innecesarias ni castigar abstenciones correctas.
- Las decisiones de alto impacto requieren revisión y controles adecuados al riesgo.

## 10. Estado de implementación

Esta versión establece la especificación y el vocabulario común. **No afirma que todos los indicadores estén instrumentados, que cada ciclo se registre automáticamente ni que exista validación independiente de las métricas.** La implementación debe avanzar por etapas: esquema de eventos, captura en un caso piloto, tablero de indicadores, auditoría de muestras y evaluación externa.

## 11. Cierre

CEUNIA no mide para acumular números. Mide para comprender la diferencia entre intención y resultado, reconocer cuándo no debe actuar, corregir sus errores y evolucionar con evidencia.

**Intención → Comprensión → Decisión → Resolución → Medición → Aprendizaje → Evolución.**

*Documento público de especificación. La publicación en GitHub aporta trazabilidad de versiones, pero no sustituye registros de propiedad intelectual ni una auditoría independiente.*
