# REQ-F-012: Timeout Exit Code and JSON Error

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§11 Timeouts & Hanging Processes](../challenges/02-critical-execution-and-reliability/11-critical-timeouts.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

When the framework's timeout fires, it MUST emit a structured JSON error to stdout before terminating the process, and MUST exit with code `7`. The error MUST include `"code": "TIMEOUT"`, the configured timeout value, and any partial progress information available from the command's registered state. The framework MUST never produce an empty stdout on timeout.

## Acceptance Criteria

- A timed-out command's stdout is valid JSON containing `"ok": false` and `"error": {"code": "TIMEOUT"}`.
- Exit code is exactly `7` after timeout.
- `meta.duration_ms` is populated with the actual elapsed time.
- If the command emitted a step manifest (see REQ-C-008), `completed_steps` is included in the timeout error.
