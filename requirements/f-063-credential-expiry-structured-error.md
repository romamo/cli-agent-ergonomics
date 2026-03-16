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
