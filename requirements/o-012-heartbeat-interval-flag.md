# REQ-O-012: --heartbeat-interval Flag

**Tier:** Opt-In | **Priority:** P2

**Source:** [§11 Timeouts & Hanging Processes](../challenges/02-critical-execution-and-reliability/11-critical-timeouts.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

For long-running commands, the framework MUST provide `--heartbeat-interval <seconds>` as a standard flag. When set, the framework emits periodic progress messages to stderr at the specified interval, formatted as `[<elapsed>s] <status_message>`. Commands declare their progress reporting by calling the framework's `progress()` API; the framework handles the throttling and formatting. This prevents the caller from mistaking a long-running command for a hang.

## Acceptance Criteria

- `--heartbeat-interval 5` causes a progress message to stderr every 5 seconds.
- The heartbeat message includes elapsed time and the most recent status from the command's `progress()` call.
- Heartbeat messages are plain text, never JSON (they are diagnostic, not structured output).
- With `--quiet`, heartbeat messages are suppressed.
