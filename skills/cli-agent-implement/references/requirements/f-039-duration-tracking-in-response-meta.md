# REQ-F-039: Duration Tracking in Response Meta

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§11 Timeouts & Hanging Processes](../challenges/02-critical-execution-and-reliability/11-critical-timeouts.md) · [§33 Observability & Audit Trail](../challenges/07-medium-observability/33-medium-observability.md)

**Addresses:** Severity: Critical (Time) / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST automatically measure wall-clock execution time for every command and inject `meta.duration_ms` (integer milliseconds) into every response. This timing MUST start when the command begins execution (after framework initialization) and MUST end immediately before JSON serialization. The timing MUST be present on both success and failure responses, including timeout and SIGTERM responses.

## Acceptance Criteria

- Every response (success, failure, timeout, cancellation) includes `meta.duration_ms`.
- `meta.duration_ms` is a non-negative integer.
- For a command that sleeps 1 second, `meta.duration_ms` is between 1000 and 1200.
