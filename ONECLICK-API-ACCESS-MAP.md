# ONECLICK — mapa de acceso a APIs (Argentina)

**Fecha de revisión:** 2026-11-14  
**Propósito:** separar APIs comerciales documentadas de permisos reales y de la capacidad de comprar como consumidor.

## Hallazgo principal

Las APIs públicas encontradas de PedidosYa y Rappi están orientadas principalmente a restaurantes/comercios asociados y a sus sistemas POS. No prueban que ONECLICK, como aplicación independiente de un consumidor, pueda consultar el catálogo completo, comparar locales y cursar pedidos en nombre de cualquier usuario.

Uber Direct es una API de logística para que un comercio cree entregas con mensajería de Uber. No equivale a una API de Uber Eats Marketplace para hacer pedidos de consumidor.

Por tanto, no declarar ninguna de estas plataformas como proveedor conectado ni como canal de compra de consumidor.

## Matriz de evidencia

| Plataforma | Capacidad documentada | Tipo de acceso | Lo que no demuestra | Estado CEUNIA |
|---|---|---|---|---|
| PedidosYa Partner API | Catálogo, promociones, recepción/gestión de pedidos de comercios asociados | Partner Portal, credenciales y habilitación de integración | Acceso universal de ONECLICK a pedidos de consumidor | INVESTIGACION_PENDIENTE |
| PedidosYa POS Integration | Webhooks y gestión de órdenes de locales asociados | Acuerdo/alta, credenciales, configuración y pruebas con PedidosYa | Checkout libre desde una app externa de consumidores | INVESTIGACION_PENDIENTE |
| Rappi POS | Integración de restaurantes con POS, menú y pedidos | Contacto/alta como aliado y proceso de integración | API abierta para que cualquier consumidor compre desde ONECLICK | INVESTIGACION_PENDIENTE |
| Uber Direct | Crear y gestionar entregas para comercios | Cuenta/credenciales Direct y disponibilidad regional confirmada | Acceso al marketplace Uber Eats ni compra de productos | INVESTIGACION_PENDIENTE |

## Fuentes oficiales consultadas

- PedidosYa Partner API: https://developer.pedidosya.com/api-specifications
- PedidosYa integración de comercios/POS: https://integrar.pedidosya.com/es/documentation/
- PedidosYa requisitos de integración POS: https://developer.pedidosya.com/es-lat/documentation/pos-partner-picking-how-to-integrate
- Rappi POS para restaurantes: https://merchants.rappi.com/es-ar/que-ofrecemos/sistema-pos
- Uber Direct overview: https://developer.uber.com/docs/deliveries/overview
- Uber Direct onboarding y disponibilidad regional: https://developer.uber.com/docs/deliveries/get-started

## Estrategia técnica recomendada

1. Mantener un núcleo independiente del proveedor: intención, normalización de pedido, restricciones, evaluación y memoria.
2. Crear adaptadores separados por producto/API y rol comercial: marketplace, POS de comercio, logística y pagos nunca se deben mezclar bajo un único permiso.
3. Para el flujo consumidor, comenzar con comercios que autoricen integración directa y checkout propio; donde no exista API autorizada, ofrecer derivación explícita al canal oficial, sin simular compra automática.
4. Para logística, evaluar Uber Direct como componente del comercio, sujeto a disponibilidad y alta.
5. No almacenar credenciales en el repositorio. Usar un gestor de secretos al desplegar y rotación/revocación documentadas.
6. Antes de cualquier operación real: sandbox, pruebas end-to-end, confirmación explícita por pedido, límites, idempotencia, webhook firmado, conciliación y recibo.

## Próximo hito que requiere acceso externo

Solicitar a PedidosYa y Rappi información de elegibilidad para integración como proveedor tecnológico/partner POS y determinar si admiten un caso de uso de agregación/checkout de terceros. Para Uber Direct, confirmar disponibilidad y alta comercial en Argentina. Sin respuesta contractual y credenciales, los adaptadores siguen en estado documental.

## Regla de honestidad

Documentación pública ≠ autorización comercial.  
API de comercio ≠ API de consumidor.  
API de logística ≠ marketplace.  
Sandbox ≠ producción.  
Un enlace de salida ≠ pedido realizado.
