> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §53

## 53. Credential Expiry Mid-Session

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Low

### The Problem

Agents often operate over sessions longer than credential lifetimes. Short-lived IAM roles (15min), JWTs (1hr), API keys (rotated by policy), and OAuth access tokens (1hr) may expire mid-task. When they do, commands start failing with 401/403, but error messages typically say "unauthorized" or "access denied" — identical to "never had permission" errors. The agent cannot distinguish "credential was never valid" (permanent failure requiring escalation) from "credential expired" (transient failure recoverable by refresh).

```bash
# Session starts — IAM role valid for 15 minutes
$ tool deploy --env prod
{"ok": true, "data": {"job_id": "dep_123"}}

# 16 minutes later
$ tool job status dep_123
{"ok": false, "error": {"code": "FORBIDDEN", "message": "Access denied"}}
# Is this: token expired? wrong permissions? job doesn't exist?
# Agent cannot tell. May retry (burns time), may abort (wrong call).

# Worse: cascade failure — every subsequent call also fails
$ tool list-resources
{"ok": false, "error": {"code": "UNAUTHORIZED", "message": "Invalid credentials"}}
```

### Impact

- Agent retries indefinitely on a non-retryable permanent permission denial
- Agent abandons a recoverable expired-token situation that just needs a refresh
- Cascading failures across all subsequent commands in the session
- Agent may attempt rollback with the same expired credential, causing rollback to also fail

### Solutions

**Auth errors MUST distinguish expiry from permission denial:**
```json
{
  "ok": false,
  "error": {
    "code": "CREDENTIALS_EXPIRED",
    "message": "Access token expired at 2024-03-11T14:15:00Z.",
    "expired": true,
    "expired_at": "2024-03-11T14:15:00Z",
    "retryable": true,
    "reauth_command": "tool auth refresh",
    "reauth_env_var": "TOOL_TOKEN"
  }
}
```

**For framework design:**
- Add `exit 10` to the standard exit code table: `10 = credentials expired (retryable with refresh)`. Exit 8 = permanent permission denied.
- Framework MUST intercept HTTP 401/403 responses and attempt to classify expiry vs permission denial before surfacing the error.
- `error.reauth_command` is a mandatory field for all auth errors — the exact command to run to recover credentials.
