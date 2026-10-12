# CEUNIA: diagnóstico técnico inicial y plan de corrección

Fecha de revisión: 2026-10-12
Base revisada: rama main, commit 0f491ca3f4717736c34424b3b2662ff029e7743c.

## Hallazgos verificados en el código consultado

1. `core/validator.py`: la coherencia se reduce a comprobar que el dato no sea nulo/vacío; el riesgo devuelve siempre `low`. No es una evaluación real de riesgo.
2. `core/router.py`: la selección entre modelos usa ponderación aleatoria con pesos iguales; no usa desempeño histórico por tipo de tarea.
3. `core/evolution.py`: `evolve()` crea un reporte con tendencia fija `stable`; la recomendación no deriva de métricas calculadas.
4. `mvp/app.py`: orquesta router, validador, memoria, metaobservador y motor evolutivo, pero la calidad de las salidas depende de las limitaciones anteriores.
5. `Untitled130.ipynb` contiene una ejecución registrada de 32 semillas en un entorno sintético. En su salida, Baseline MAE=0.078204 y Core MAE=0.074658 (mejora relativa reportada 4.53%). Esto es evidencia de un resultado de benchmark sintético registrado, no una demostración de rentabilidad ni de predicción financiera real.
6. `Untitled132.ipynb` registra un experimento con datos FRED/S&P 500 y declara que no se observa mejora OOS: ganancia reportada -0.058%, p=0.747. No debe presentarse como mejora.

## Cambio propuesto en esta rama

Se añade `core/validator_evidence.py`, un validador de registros estructurados que exige objetivo, evidencia y puntuaciones numéricas acotadas para riesgo, incertidumbre y calidad de evidencia. Si faltan campos, los rangos son inválidos o se superan umbrales, el resultado es HOLD. No sustituye revisión semántica humana ni pretende clasificar texto libre.

Se añaden pruebas unitarias para aprobación de un registro completo, fallo cerrado, riesgo alto, evidencia ausente, rangos inválidos, configuración de política, hash y memoria de evaluaciones.

## Próximos pasos

- Ejecutar estas pruebas en el entorno del repositorio y configurar CI.
- Diseñar el router con métricas por tipo de tarea, tamaños de muestra y comparación contra baseline.
- Hacer que evolución calcule recomendaciones a partir de métricas observadas, con rollback y registro CER.
- Reproducir el benchmark sintético y mantener separado el experimento financiero real.
- No tocar main hasta revisar y aprobar un pull request.
