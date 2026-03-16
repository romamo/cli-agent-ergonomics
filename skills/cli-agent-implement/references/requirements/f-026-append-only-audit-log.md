# REQ-F-026: Append-Only Audit Log

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§33 Observability & Audit Trail](../challenges/07-medium-observability/33-medium-observability.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: High / Context: Medium

---

## Description

The framework MUST write an append-only audit log entry for every command invocation to a JSONL file at a well-known, configurable path (default: `~/.local/share/<toolname>/audit.jsonl`). Each entry MUST include: timestamp, command name, sanitized arguments (with secret fields redacted), exit code, duration_ms, trace_id, and request_id. The audit log MUST be written regardless of whether the command succeeded or failed.

## Acceptance Criteria

- After any command invocation, the audit log file contains a new JSONL entry.
- The entry for a command invoked with a secret argument does not contain the secret value.
- The audit log is valid JSONL (one JSON object per line, newline-delimited).
- The audit log is written even when the command exits non-zero.
