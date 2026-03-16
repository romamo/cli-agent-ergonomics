# REQ-F-024: Request ID and Trace ID in Every Response

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§33 Observability & Audit Trail](../challenges/07-medium-observability/33-medium-observability.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: High / Context: Medium

---

## Description

The framework MUST generate a unique `meta.request_id` for every command invocation. The framework MUST read `TOOL_TRACE_ID` from the environment and propagate it as `meta.trace_id`. Both values MUST appear in every response. The framework MUST include `meta.command` (the command name) and `meta.timestamp` (ISO 8601 invocation time) in every response.

## Acceptance Criteria

- Every response includes `meta.request_id`, which is unique across all invocations.
- When `TOOL_TRACE_ID=abc123` is set, every response includes `meta.trace_id: "abc123"`.
- `meta.command` matches the name of the command that was invoked.
- `meta.timestamp` is a valid ISO 8601 datetime.
