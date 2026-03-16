# REQ-C-003: Mutating Commands Declare effect Field

**Tier:** Command Contract | **Priority:** P0

**Source:** [§12 Idempotency & Safe Retries](../challenges/02-critical-execution-and-reliability/12-critical-idempotency.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

Every command with `danger_level` of `mutating` or `destructive` MUST include an `effect` field in its success response. The `effect` value MUST be one of: `"created"`, `"updated"`, `"deleted"`, `"noop"`. Command authors MUST determine and set the correct value based on what actually occurred. The framework MUST validate that the `effect` field is present and has a valid value for all non-safe commands.

## Acceptance Criteria

- A mutating command response always includes `"effect"` at the top level of the envelope.
- `effect: "noop"` is returned when the operation was a no-op (e.g., already at desired state).
- `effect: "created"` vs `effect: "updated"` is accurate (not always one or the other).
- The framework raises a registration or runtime error if a mutating command omits `effect`.
