# REQ-F-025: TOOL_TRACE_ID Environment Variable Propagation

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§33 Observability & Audit Trail](../challenges/07-medium-observability/33-medium-observability.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: High / Context: Medium

---

## Description

The framework MUST read `TOOL_TRACE_ID` from the environment at startup and associate it with the current invocation. The framework MUST also pass `TOOL_TRACE_ID` to all child processes spawned during the command. All internal framework log entries written to stderr and the audit log MUST include the trace ID when set.

## Acceptance Criteria

- A child process spawned by the framework inherits `TOOL_TRACE_ID`.
- Framework-emitted log lines (stderr) include the trace ID when `TOOL_TRACE_ID` is set.
- Audit log entries include the trace ID.
