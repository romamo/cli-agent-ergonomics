# REQ-C-007: Mutating Commands Accept --idempotency-key

**Tier:** Command Contract | **Priority:** P1

**Source:** [§12 Idempotency & Safe Retries](../challenges/02-critical-execution-and-reliability/12-critical-idempotency.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

Every command with `danger_level: "mutating"` or `"destructive"` MUST accept an `--idempotency-key <string>` argument. The command MUST use this key to detect and short-circuit duplicate invocations, returning the original result with `effect: "noop"` and the original response data. When no key is supplied, the framework MAY auto-generate one (deterministic, based on command + args + session) or MUST document that the operation is not deduplication-safe.

## Acceptance Criteria

- Invoking a mutating command twice with the same `--idempotency-key` returns `effect: "noop"` on the second call.
- The second call's response `data` matches the first call's response `data`.
- An auto-generated idempotency key is deterministic for the same command arguments within a session.
