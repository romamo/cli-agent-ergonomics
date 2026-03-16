# REQ-F-013: SIGTERM Handler Installation

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§16 Signal Handling & Graceful Cancellation](../challenges/02-critical-execution-and-reliability/16-high-signal-handling.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST install a SIGTERM signal handler for every command at startup. On SIGTERM, the handler MUST: invoke the command's registered `cleanup()` hook, release any framework-managed locks, emit a partial-result JSON object to stdout (with `"ok": false`, `"partial": true`, `"error": {"code": "CANCELLED"}`), flush stdout, and exit with code `143` (128 + SIGTERM). The handler MUST be re-entrant safe (a second SIGTERM during cleanup MUST not cause a double-write).

## Acceptance Criteria

- `kill -TERM <pid>` on a running command causes stdout to contain a valid JSON cancellation response.
- Exit code after SIGTERM is exactly `143`.
- All framework-managed lock files are released after SIGTERM.
- A second SIGTERM during cleanup does not produce duplicate JSON output.
