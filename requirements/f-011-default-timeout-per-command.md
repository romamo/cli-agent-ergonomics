# REQ-F-011: Default Timeout Per Command

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§11 Timeouts & Hanging Processes](../challenges/02-critical-execution-and-reliability/11-critical-timeouts.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST apply a default wall-clock timeout to every command execution. The default value MUST be configurable at the framework level and overridable per command. A command that exceeds its timeout MUST be terminated by the framework, not left to run indefinitely. The timeout MUST be enforced even if the command itself does not implement any timeout logic.

## Acceptance Criteria

- A command that sleeps indefinitely exits within `default_timeout + 5s` without manual intervention.
- The framework's timeout mechanism works even if the command's code is blocked on I/O.
- The timeout value used for each execution is recorded in `meta.timeout_ms`.
