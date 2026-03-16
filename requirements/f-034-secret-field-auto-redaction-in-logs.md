# REQ-F-034: Secret Field Auto-Redaction in Logs

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§24 Authentication & Secret Handling](../challenges/03-critical-security/24-critical-auth-secrets.md)

**Addresses:** Severity: Critical / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST automatically redact any argument or field whose name matches a secret pattern (case-insensitive substrings: `token`, `secret`, `password`, `key`, `credential`, `auth`) before writing to the audit log or stderr. Redaction MUST replace the value with `"[REDACTED]"`. This MUST apply to: command-line argument values, environment variable values echoed in diagnostics, and JSON response fields that match the pattern.

## Acceptance Criteria

- An argument `--api-token abc123` appears as `--api-token [REDACTED]` in the audit log.
- A response field `"password": "secret"` appears as `"password": "[REDACTED]"` in the audit log.
- The actual command execution is not affected by redaction (redaction is log-layer only).
- Redaction applies to field names matched case-insensitively.
