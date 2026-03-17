# REQ-F-063: Credential Expiry Structured Error

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§53 Credential Expiry Mid-Session](../challenges/01-critical-ecosystem-runtime-agent-specific/53-critical-credential-expiry.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Low

---

## Description

The framework MUST distinguish between three credential failure modes and emit structured errors with distinct exit codes and machine-readable fields for each: (1) Never authenticated — exit 8, `error.code: UNAUTHENTICATED`, with `hint` pointing to the login command; (2) Credentials expired — exit 10, `error.code: CREDENTIALS_EXPIRED`, with `error.expires_at` (ISO-8601), `error.refresh_command` (exact CLI invocation to renew); (3) Insufficient permissions — exit 8, `error.code: PERMISSION_DENIED`, with `error.required_permission`. The framework intercepts HTTP 401/403 responses from its HTTP client and maps them to these structured errors automatically. Commands declare their required credential scopes via `required_scopes: []`.

## Acceptance Criteria

- An expired token produces exit 10 with `error.code: "CREDENTIALS_EXPIRED"` and `error.refresh_command`.
- A missing token produces exit 8 with `error.code: "UNAUTHENTICATED"` and `hint` pointing to the auth command.
- A valid token with insufficient scope produces exit 8 with `error.code: "PERMISSION_DENIED"` and `error.required_permission`.
- An agent can distinguish expiry from denial by exit code alone (10 vs 8) without parsing error text.

---

## Schema

**Types:** [`response-envelope.md`](../schemas/response-envelope.md) · [`exit-code.md`](../schemas/exit-code.md)

The framework maps HTTP 401/403 responses to structured `ErrorDetail` objects. Credential expiry uses `TIMEOUT (10)`; missing or invalid credentials use `AUTH_REQUIRED (8)`.

---

## Wire Format

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "CREDENTIALS_EXPIRED",
    "message": "Access token expired at 2025-03-01T00:00:00Z",
    "retryable": true,
    "expires_at": "2025-03-01T00:00:00Z",
    "refresh_command": "mytool auth refresh"
  },
  "warnings": [],
  "meta": { "duration_ms": 120 }
}
```

---

## Example

Framework-Automatic: no command author action needed. The framework intercepts HTTP 401/403 from its HTTP client and maps them to the appropriate structured error.

```
# Expired token → exit 10, CREDENTIALS_EXPIRED
$ mytool deploy --json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "CREDENTIALS_EXPIRED",
    "message": "Token expired at 2025-03-01T00:00:00Z",
    "retryable": true,
    "expires_at": "2025-03-01T00:00:00Z",
    "refresh_command": "mytool auth refresh"
  },
  ...
}
→ exit 10; agent runs refresh_command then retries

# Missing token → exit 8, UNAUTHENTICATED
$ mytool deploy --json
{
  "ok": false, "data": null,
  "error": { "code": "UNAUTHENTICATED", "hint": "Run: mytool auth login", "retryable": false },
  ...
}
→ exit 8; agent runs auth login flow
```

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-001](f-001-standard-exit-code-table.md) | F | Provides: `AUTH_REQUIRED (8)` and `TIMEOUT (10)` exit codes used for credential failures |
| [REQ-F-004](f-004-consistent-json-response-envelope.md) | F | Provides: `ResponseEnvelope` shape for the credential error responses |
| [REQ-F-037](f-037-network-error-context-block.md) | F | Composes: network-level HTTP error context is merged into the credential error detail |
| [REQ-F-034](f-034-secret-field-auto-redaction-in-logs.md) | F | Composes: credential values in error details are redacted from logs |
