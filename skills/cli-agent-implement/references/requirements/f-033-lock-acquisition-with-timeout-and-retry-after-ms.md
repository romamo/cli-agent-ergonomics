# REQ-F-033: Lock Acquisition with Timeout and retry_after_ms

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§15 Race Conditions & Concurrency](../challenges/02-critical-execution-and-reliability/15-high-race-conditions.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

When a command acquires a framework-managed advisory lock, the framework MUST enforce a configurable acquisition timeout. If the lock cannot be acquired within the timeout, the framework MUST emit a structured JSON error containing `"code": "LOCK_HELD"`, the PID and age of the lock holder, and a `retry_after_ms` value. Lock files MUST be released by the framework's exit and SIGTERM handlers.

## Acceptance Criteria

- A command waiting for a held lock exits with a `LOCK_HELD` JSON error after the configured timeout.
- The error includes `retry_after_ms`.
- The lock is released when the holding process exits normally.
- The lock is released when the holding process receives SIGTERM.
