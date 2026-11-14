# ONECLICK — All in one click
## Economía de datos vivos e interpretación en tiempo real
**Documento de producto y arquitectura | CEUNIA Ω | v0.1**

## 1. Tesis de producto

ONECLICK evoluciona de una interfaz de pedidos a una infraestructura de interpretación y resolución. Su función es transformar una intención expresada en lenguaje natural en una propuesta útil, verificable y accionable, usando datos vivos con procedencia, vigencia, contexto y autorización.

**Posicionamiento:** ONECLICK es una puerta de entrada operativa a una economía de datos vivos: conecta necesidades con información vigente, capacidades disponibles y resultados verificables.

No se afirma que ONECLICK sea el origen histórico de toda la economía de datos. Se define como un posible origen operativo de un nuevo circuito de intercambio de valor basado en interpretación y resolución.

## 2. Qué significa “dato vivo”

Un dato es vivo cuando no se trata como una verdad permanente. Debe poder responder:

- **Qué:** valor, entidad o condición observada.
- **Quién / qué fuente:** comercio, proveedor, dispositivo, usuario o sistema autorizado.
- **Dónde:** región o alcance de validez.
- **Cuándo:** instante de observación.
- **Hasta cuándo:** vencimiento o política de frescura.
- **Con qué permiso:** base de acceso, uso y eventual compartición.
- **Con qué confianza:** evidencia, estado de verificación y limitaciones.

Ejemplo: “Pizza mozzarella disponible a ARS 8.500” no es suficiente por sí solo. La información útil identifica comercio, producto, moneda, stock observado, fuente, región, hora de consulta y vigencia. El sistema debe distinguir precio observado de precio final y disponibilidad observada de reserva confirmada.

## 3. El ciclo ONECLICK

1. **Intención:** la persona expresa qué necesita, con la mínima fricción posible.
2. **Interpretación:** el sistema identifica objetivo, entidades, cantidades, modalidad, restricciones y ambigüedades.
3. **Metaobservación:** evalúa su propia interpretación, detecta faltantes, contradicciones y riesgo.
4. **Obtención de datos vivos:** consulta fuentes autorizadas y registra procedencia, frescura, permisos y calidad.
5. **Resolución:** filtra restricciones obligatorias y compara alternativas con criterios transparentes.
6. **Propuesta:** construye un objeto verificable, identificable y sujeto a vencimiento.
7. **Punto Albedrío:** la persona revisa y confirma antes de cualquier acción externa relevante.
8. **Ejecución:** un adaptador autorizado ejecuta solo la operación confirmada.
9. **Resultado:** se registra la respuesta real de la contraparte, con referencia externa e idempotencia.
10. **Memoria y evolución:** se conserva evidencia y se mejora el proceso dentro de permisos explícitos.

## 4. Economía de datos vivos

La unidad económica central no es la acumulación de datos personales. Es la **resolución útil producida con información autorizada y vigente**.

El valor puede distribuirse entre:
- La persona, que ahorra tiempo, pasos y costo de búsqueda.
- El comercio o proveedor, que recibe una intención mejor interpretada y una oportunidad cualificada.
- El proveedor de datos, que puede recibir compensación por información autorizada, fiable y actualizada.
- ONECLICK, que aporta interpretación, coordinación, comparación, trazabilidad y resolución.

Modelos posibles, sujetos a acuerdos y validación:
- comisión transparente por transacción completada;
- tarifa por resolución o servicio;
- suscripción para comercios y organizaciones;
- acceso a capacidades de integración y automatización;
- compensación a proveedores de datos cuando exista licencia y permiso.

No se monetizan datos personales por defecto. No se vende ni comparte información identificable sin base legal, consentimiento cuando corresponda y controles de finalidad, minimización, seguridad y revocación.

## 5. Arquitectura por capas

| Capa | Función | Evidencia requerida |
|---|---|---|
| Interfaz ONECLICK | Capturar intención con mínima expresión | Entrada y contexto explícitos |
| Interpretación | Extraer objetivo, entidades y restricciones | Interpretación revisable |
| Metaobservación CEUNIA | Detectar ambigüedad, riesgo y contradicción | Razón y estado de decisión |
| Conectores de datos | Consultar fuentes autorizadas | Fuente, permiso, timestamp y vigencia |
| Motor de resolución | Filtrar, comparar y priorizar | Criterios, límites y explicación |
| Propuesta | Congelar una alternativa verificable | ID/hash, precio, moneda, modalidad y vencimiento |
| Punto Albedrío | Exigir decisión humana | Confirmación explícita ligada a propuesta |
| Adaptador de ejecución | Operar con proveedor autorizado | Idempotencia y referencia externa |
| Memoria viva | Persistir propuestas, decisiones y resultados | Historial auditable y política de retención |

CEUNIA aporta la inteligencia de observación, memoria, evaluación y evolución. ONECLICK es la interfaz y el circuito de resolución. Los proveedores externos siguen siendo dueños de sus sistemas y datos.

## 6. Reglas no negociables

1. No inventar disponibilidad, precio, API, permiso ni conexión.
2. No presentar datos vencidos como actuales.
3. No confundir cotización con precio final, confirmación con pedido enviado ni pedido enviado con pedido aceptado.
4. No cambiar modalidad, cantidad, destino o producto sin autorización.
5. No ejecutar operaciones externas sin confirmación explícita y autorización válida.
6. Toda acción repetible debe usar idempotencia local y, cuando corresponda, remota.
7. Toda interpretación relevante debe poder revisarse y corregirse.
8. Recoger y conservar solo los datos necesarios para la finalidad declarada.
9. Mantener trazabilidad de fuente, cambios, decisiones, resultados y errores.
10. Permitir abstenerse, pedir aclaración o no activar cuando la evidencia sea insuficiente.

## 7. Métricas de economía de resolución

- Tiempo desde intención hasta propuesta verificable.
- Porcentaje de interpretaciones aceptadas sin corrección.
- Tasa de aclaraciones necesarias y ambigüedades detectadas.
- Frescura y cobertura de los datos consultados.
- Diferencia entre precio observado y precio final.
- Tasa de propuestas disponibles al momento de confirmar.
- Conversión de propuesta a confirmación y de confirmación a aceptación real.
- Errores, duplicados, rechazos y expiraciones.
- Costo por resolución completada.
- Beneficio verificable para persona y proveedor.
- Incidentes de privacidad, permisos y seguridad.

La optimización debe minimizar fricción, tiempo y costo sin sacrificar precisión, consentimiento, seguridad ni capacidad de revisión.

## 8. Secuencia de madurez

**Nivel 1 — Prototipo verificable:** interpretación, catálogo de prueba, propuesta, confirmación y memoria local.  
**Nivel 2 — Fuente real de solo lectura:** un comercio autorizado, catálogo y precios con vigencia.  
**Nivel 3 — Propuesta comercial real:** costos completos, disponibilidad actualizada y condiciones transparentes.  
**Nivel 4 — Ejecución autorizada:** envío de pedido con idempotencia remota y respuesta verificable.  
**Nivel 5 — Red de resolución:** varios proveedores, regiones y categorías, con interoperabilidad y economía de datos bajo permisos.  
**Nivel 6 — Ecosistema adaptativo:** aprendizaje de resultados, preferencias controladas por la persona y optimización transversal auditable.

No se declara alcanzado un nivel por tener código preparado para él. Cada nivel requiere evidencia de funcionamiento en su entorno real.

## 9. Primer piloto recomendado

Comenzar con una sola categoría y un comercio de Mar del Plata que autorice formalmente la integración.

Fases:
1. Acordar alcance, permisos, condiciones, API o mecanismo oficial.
2. Consultar catálogo real en modo solo lectura.
3. Verificar precio, disponibilidad, modificadores, modalidad y vigencia.
4. Mostrar propuesta transparente, sin ejecutar.
5. Probar confirmación y expiración.
6. Habilitar envío solo tras autorización comercial y revisión de seguridad.
7. Registrar respuesta real, referencia externa y recibo.
8. Medir beneficio, errores y costo operativo.

## 10. Definición final

**ONECLICK — All in one click.**

Una intención. Una interpretación revisable. Datos vivos. Una propuesta verificable. Una confirmación humana. Una resolución trazable.

**La economía de datos vivos empieza cuando la información deja de acumularse y empieza a resolver, con permiso, contexto y evidencia.**
