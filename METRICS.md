# CEUNIA Ω — Métricas y medición evolutiva

CEUNIA evalúa inteligencia no solo por rendimiento, sino también por coherencia, adaptabilidad, seguridad, autonomía y capacidad de corregir su trayectoria con evidencia.

La especificación transversal y operativa está en [MEDICION-OMEGA.md](MEDICION-OMEGA.md).

## Ciclo de medición

**Intención → Comprensión → Decisión → Resolución → Medición → Aprendizaje → Evolución.**

La medición incluye acciones y no acciones: actuar, esperar, consultar, solicitar autorización y abstenerse.

## Indicadores arquitectónicos exploratorios

### Coherencia (C)

Alineación entre trayectoria, decisiones, memoria y resultados. La definición de cálculo debe establecerse para cada caso de uso antes de comparar versiones.

### Potercia (P)

Capacidad dinámica de corregir o adaptar una trayectoria ante una desviación, considerando el tiempo y el costo de corrección.

### Puntos de Revelación Evolutiva (PRE)

Eventos que aportan información nueva y abren alternativas de decisión. Deben documentarse mediante casos observables.

### Serendipia (S)

Descubrimientos no planificados que resultan útiles y verificables.

### MetaSerendipia (MS)

Capacidad de diseñar condiciones que favorezcan descubrimientos útiles sin inducir ruido, sesgo o acciones innecesarias.

### Relación Coherencia–Potercia (CPR)

Relación exploratoria entre estabilidad y velocidad de adaptación. No debe interpretarse como índice validado hasta definir escalas, pesos y pruebas.

### Índice Global de Evolución (GEI)

Combinación propuesta de dimensiones de coherencia, Potercia, PRE, Serendipia y MetaSerendipia. Los pesos y el método requieren calibración y validación por dominio.

## Reglas de rigor

- No publicar puntuaciones sin método, denominador, conjunto de casos y ventana temporal.
- Separar métricas exploratorias de indicadores operativos validados.
- No confundir confianza del modelo con verdad ni evidencia.
- Desagregar resultados por riesgo y tipo de tarea.
- Registrar abstenciones adecuadas para no premiar la activación innecesaria.
- Comparar versiones en condiciones equivalentes y comprobar regresiones.

Los indicadores de implementación, registro mínimo, revisión humana y condiciones de no activación se detallan en [MEDICION-OMEGA.md](MEDICION-OMEGA.md).
