# REQ-O-030: tool audit-log Built-In Command

**Tier:** Opt-In | **Priority:** P2

**Source:** [§33 Observability & Audit Trail](../challenges/07-medium-observability/33-medium-observability.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: High / Context: Medium

---

## Description

The framework MUST provide a built-in `tool audit-log` command that queries the audit log (REQ-F-026). The command MUST accept `--since <duration or ISO datetime>`, `--command <name>`, `--trace-id <id>`, `--output jsonl`, and `--limit <n>`. Each returned entry MUST contain: timestamp, command, sanitized parameters, exit code, duration_ms, trace_id, request_id, and operator (session identifier if available).

## Acceptance Criteria

- `tool audit-log --since 1h --output jsonl` returns all invocations from the past hour, one per line.
- `tool audit-log --trace-id abc123` returns only entries with that trace ID.
- Secret field values are redacted in all audit log query results.
- `--limit 100` returns at most 100 entries.
