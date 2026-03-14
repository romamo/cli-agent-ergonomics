# REQ-O-011: --rollback-on-failure Flag

**Tier:** Opt-In | **Priority:** P2

**Source:** [§13 Partial Failure & Atomicity](../challenges/02-critical-execution-and-reliability/13-critical-partial-failure.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

Commands that support rollback MUST declare `rollback_available: true` and implement a `rollback()` hook. The framework MUST provide `--rollback-on-failure` as a standard flag for such commands. When this flag is passed and a step fails, the framework invokes the command's `rollback()` hook before exiting. The response MUST indicate whether rollback succeeded via `rollback_status: "completed" | "failed" | "not_attempted"`.

## Acceptance Criteria

- `--rollback-on-failure` with a mid-step failure triggers the `rollback()` hook.
- The response includes `rollback_status`.
- A rollback failure is reported with `rollback_status: "failed"` and details in the response.
- The exit code after a failed step with successful rollback is `3` (not `0`).
