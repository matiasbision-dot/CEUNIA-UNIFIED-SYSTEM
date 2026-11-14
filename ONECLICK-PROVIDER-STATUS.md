# ONECLICK provider and execution status

This file distinguishes architecture from live integrations. No commercial provider is represented as connected or authorized by this registry.

## Provider registry baseline

| Provider | Category | Region | State | Evidence |
|---|---|---|---|---|
| DemoAdapter | Food quote | Mar del Plata | SANDBOX_VERIFICADO | Automated fixture tests and CI |
| Commercial providers | Not yet mapped | Argentina | INVESTIGACION_PENDIENTE | No live API credentials or end-to-end evidence |

## Status semantics

- IDENTIFICADO: name/category/region recorded only.
- INVESTIGACION_PENDIENTE: API, commercial terms, regional coverage or legal requirements not yet checked.
- ACCESO_PENDIENTE: documentation may exist, but credentials/permission are missing.
- EN_DESARROLLO: adapter is being implemented, not yet verified.
- SANDBOX_VERIFICADO: sandbox behavior tested with reproducible evidence.
- PRODUCCION_VERIFICADA: production capability and end-to-end evidence independently recorded.
- BLOQUEADO: a documented dependency or restriction prevents progress.

## Execution gate

core/execution.py defines a fail-closed gateway. It requires:
1. Explicit user confirmation for the specific action.
2. A provider record marked PRODUCCION_VERIFICADA with production evidence.
3. An adapter explicitly capable of production ordering.
4. Amount, currency, destination and idempotency key.
5. A durable ledger whose reserve operation is atomic and whose outcomes are persisted.
6. A provider receipt matching the provider and idempotency key.

The repository includes only fake test adapters and an in-memory test ledger. These are not suitable for real purchases. A timeout or malformed receipt returns RECONCILIATION_REQUIRED; the idempotency key remains reserved to prevent blind retries.

## Current truthful boundary

Quote comparison is demonstrated with fictional sandbox data. No real merchant API, payment processor, delivery network, customer account, credential, or production order has been connected or tested. A real integration must be implemented and separately verified for each provider, operation and region.
