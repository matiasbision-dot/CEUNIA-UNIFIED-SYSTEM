# CEUNIA ONECLICK — Prototipo v0.2

- Fecha de avance: 2026-10-29
- Autor/proponente del proyecto: Néstor Matías de la Peña
- Repositorio: CEUNIA-UNIFIED-SYSTEM
- Estado: demo web inicial publicada en el repositorio; no es un servicio de contratación operativo.

## Alcance de esta entrega

Se incorpora `ONECLICK/index.html`, una demo web adaptable a móviles para ilustrar la idea central: la persona expresa una necesidad en lenguaje natural y el flujo puede solicitar permiso del navegador para acceder a la ubicación.

## Qué permite comprobar

1. Escribir una solicitud o elegir un ejemplo (taxi, pizza u hotel).
2. Activar el flujo con el botón ONE CLICK.
3. Solicitar ubicación mediante el permiso estándar del navegador.
4. Mostrar el pedido y si la ubicación se compartió, sin enviar datos a terceros.

## Límites explícitos

- No consulta proveedores ni disponibilidad en tiempo real.
- No cotiza precios, no reserva, no despacha transporte y no cobra.
- La ubicación solo se usa en el navegador para esta demostración; no se envía a un backend.
- La geolocalización suele requerir HTTPS o localhost y permiso del usuario.

## Próximo hito

Probar la demo en un navegador móvil servido mediante HTTPS; después definir e implementar una primera integración autorizada con un proveedor real en una zona piloto, incluyendo precio, consentimiento, confirmación y trazabilidad del resultado.

## Trazabilidad

Esta nota documenta el alcance de la entrega v0.2. El historial de commits de GitHub permite seguir los cambios del repositorio, pero no sustituye registros legales ni demuestra por sí solo derechos exclusivos sobre la idea.
