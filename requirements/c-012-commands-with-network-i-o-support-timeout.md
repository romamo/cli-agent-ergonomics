# REQ-C-012: Commands with Network I/O Support --timeout

**Tier:** Command Contract | **Priority:** P0

**Source:** [§11 Timeouts & Hanging Processes](../challenges/02-critical-execution-and-reliability/11-critical-timeouts.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

Every command that performs network I/O or any potentially long-running blocking operation MUST accept `--timeout <duration>` and `--connect-timeout <duration>` flags (where applicable). The framework registers these flags automatically for commands that declare `has_network_io: true`. Command authors MUST pass the configured timeout to all network calls; the framework MUST enforce that no network call is made without a finite timeout.

## Acceptance Criteria

- A command with `has_network_io: true` always accepts `--timeout`.
- The configured `--timeout` value is passed to all network requests made by the command.
- A network call with no explicit timeout is flagged by the framework's static analysis rule.
- `--timeout 0` explicitly opts into no timeout (must be a deliberate choice, not the default).
