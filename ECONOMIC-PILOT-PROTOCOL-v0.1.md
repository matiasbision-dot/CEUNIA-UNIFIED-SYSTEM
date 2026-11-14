# ONECLICK — Protocolo de piloto económico
**Versión:** 0.1 · **Estado:** protocolo propuesto; piloto no iniciado

## 1. Pregunta de evaluación
¿ONECLICK mejora la resolución de una intención de compra frente a un baseline comparable, con datos autorizados, vigentes y verificables, sin aumentar riesgos ni ocultar costos?

## 2. Alcance inicial
- Una pizzería independiente, solo después de autorización.
- Una categoría y un flujo acotado.
- Consulta y propuesta en modo seguro.
- Ningún pedido real ni pago sin autorización específica y controles adicionales.
- No extrapolar resultados a otros comercios, categorías o ciudades.

## 3. Diseño comparativo
Definir antes de medir:
- misma intención, artículos, cantidades y modificadores;
- misma modalidad (retiro o delivery), zona y ventana temporal;
- mismo criterio de inicio/fin del cronómetro;
- mismo tratamiento de espera y reintentos;
- misma composición de precio final;
- baseline documentado y evidencia verificable.

Registrar protocolo, versión de software, versión del catálogo, fecha, zona horaria y exclusiones antes de comenzar. No modificar el baseline después de observar resultados sin dejar una nueva versión justificada.

## 4. Cinco dimensiones económicas
### 4.1 Tiempo ahorrado
`tiempo_baseline_segundos - tiempo_ONECLICK_segundos`.
Valor positivo: menor tiempo con ONECLICK. Negativo: ONECLICK tardó más. Definir si incluye espera externa y medir ambos lados con el mismo criterio.

### 4.2 Errores evitados
`errores_baseline - errores_ONECLICK`.
Definir taxonomía antes del piloto: interpretación, cantidad, modificador, modalidad, precio/cargo, disponibilidad, duplicación y dato vencido. Un valor negativo significa más errores con ONECLICK. No contar como evitado un error sin evidencia.

### 4.3 Mejora de precio/resultado
`total_comparable_baseline - total_comparable_ONECLICK`, en la misma moneda y para el mismo resultado. Incluir cargos de entrega, adicionales, descuentos aplicables e impuestos cuando correspondan. No comparar subtotal con total final. Si no hay comparabilidad, marcar NO MEDIDO.

### 4.4 Contribución de fuente
Identificar fuente, registro, vigencia y evidencia de cómo influyó materialmente en la propuesta o resultado. Consultar o mostrar una fuente no basta para atribuir contribución.

### 4.5 Distribución de valor
Registrar solo términos expresamente autorizados y su referencia documental. Estados posibles: NO DEFINIDA, TÉRMINOS AUTORIZADOS, RECONCILIADA. No inferir porcentajes, comisiones ni reparto de ingresos.

## 5. Evidencia mínima por observación
- identificador de prueba y consentimiento aplicable;
- intención original y versión interpretada, minimizando datos personales;
- baseline y método de medición;
- propuesta y snapshot del catálogo;
- fuentes y timestamps;
- tiempos, errores y totales comparables;
- resultado externo, si existiera, respaldado por comprobante;
- hashes de artefactos y registro de eventos;
- desviaciones, exclusiones y limitaciones.

## 6. Reglas de abstención
No emitir conclusión positiva si falta baseline, autorización, procedencia, vigencia, moneda, total comparable o evidencia de resultado. Marcar explícitamente NO MEDIDO / NO VERIFICADO. Los datos de fixture solo prueban comportamiento de software, no valor económico real.

## 7. Análisis y reporte
Informar tamaño de muestra, distribución y casos fallidos, no solo promedios. Separar resultados observados, inferencias y limitaciones. No monetizar tiempo ni errores sin método de valoración aprobado. No afirmar causalidad con una muestra insuficiente o diseño no comparable.

## 8. Seguridad y protección
Minimizar datos, limitar acceso, definir retención y borrado, y no recolectar datos de clientes finales salvo necesidad, base y autorización documentadas. Los incidentes suspenden el piloto hasta revisión.

## 9. Puertas de avance
- **G0:** comercio identificado y autorización firmada.
- **G1:** catálogo/fuentes validados y protocolo aprobado.
- **G2:** pruebas READ_ONLY/PROPOSAL superadas.
- **G3:** evaluación económica con baseline y evidencia suficiente.
- **G4:** cualquier ejecución externa, solo con autorización separada, revisión técnica y controles operativos.

## 10. Estado
Piloto NO INICIADO. No hay resultados económicos reales atribuidos a ONECLICK por este documento.
