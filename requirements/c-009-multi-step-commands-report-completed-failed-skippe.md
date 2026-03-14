# REQ-C-009: Multi-Step Commands Report completed/failed/skipped

**Tier:** Command Contract | **Priority:** P1

**Source:** [§13 Partial Failure & Atomicity](../challenges/02-critical-execution-and-reliability/13-critical-partial-failure.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

Any command that operates on a batch of items MUST include a `summary` object in its response containing `total`, `succeeded`, and `failed` integer counts. For each individual item that failed, the response MUST include per-item error details within `results[]`. This MUST allow a caller to determine exactly which items succeeded and which failed, enabling safe retry of only the failed items.

## Acceptance Criteria

- A batch command response includes `summary.total`, `summary.succeeded`, `summary.failed`.
- Each item in `results[]` includes `ok: true/false` and, when false, an `error` object.
- The item-level `error` object follows the standard error structure (code, message, retryable).
- The exit code for a partial batch success is non-zero (not `0`).
