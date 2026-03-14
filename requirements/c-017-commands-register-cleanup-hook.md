# REQ-C-017: Commands Register cleanup() Hook

**Tier:** Command Contract | **Priority:** P1

**Source:** [§16 Signal Handling & Graceful Cancellation](../challenges/02-critical-execution-and-reliability/16-high-signal-handling.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

Every command that acquires resources (locks, temp files, network connections, child processes) MUST register a `cleanup()` hook with the framework. The framework invokes this hook on normal exit, SIGTERM, and timeout. The `cleanup()` hook MUST be idempotent (safe to call multiple times). Command authors MUST use the framework's resource acquisition APIs, which automatically register cleanup handlers.

## Acceptance Criteria

- A command that acquires a lock has the lock released on normal exit, SIGTERM, and timeout.
- A `cleanup()` hook called twice produces the same end state as calling it once.
- A command that does not acquire any resources MAY register a no-op cleanup hook.
- The framework warns at development time if a command acquires a tracked resource without a cleanup hook.
