# REQ-F-014: SIGPIPE Handler Installation

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§16 Signal Handling & Graceful Cancellation](../challenges/02-critical-execution-and-reliability/16-high-signal-handling.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST install a SIGPIPE handler that suppresses the default behavior (which raises an error or produces a traceback in some runtimes). When SIGPIPE is received, the command MUST exit silently and cleanly with exit code `0` (broken pipe is not an error — the consumer simply stopped reading). No stack trace or error message MUST be emitted.

## Acceptance Criteria

- `tool list-large | head -1` exits cleanly with no error output on stderr.
- Exit code after SIGPIPE from a pipe consumer closing early is `0`.
- No `BrokenPipeError` traceback appears on stderr.
