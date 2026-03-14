> **Part III: Errors & Discoverability** | Challenge §19

## 19. Retry Hints in Error Responses

**Severity:** High | **Frequency:** Very Common | **Detectability:** Medium | **Token Spend:** High | **Time:** High | **Context:** Medium

### The Problem

When a command fails, the agent decides: retry immediately, retry after delay, retry with different args, or give up. Without explicit guidance, agents either retry everything (wasting resources, amplifying rate-limit violations) or give up on recoverable failures.

**Agent retrying a non-retryable error:**
```bash
$ tool create-user --email "not-an-email"
{"ok": false, "error": {"code": "VALIDATION_ERROR", "message": "Invalid email"}}
exit 1

# Agent retries 3 times with identical args
# Each retry fails identically — wasted calls, wasted tokens
```

**Agent giving up on a retryable error:**
```bash
$ tool call-api
{"ok": false, "error": {"code": "SERVICE_UNAVAILABLE", "message": "Try again later"}}
exit 1

# Agent marks task as failed and escalates to user
# But the service recovered 2 seconds later
```

**Rate limit with no backoff hint:**
```bash
$ tool sync-data
{"ok": false, "error": {"code": "RATE_LIMITED", "message": "Too many requests"}}
exit 9

# Agent retries immediately → hits rate limit again → retry loop
```

### Impact

- Retry amplifies the original problem (rate limits, load)
- No-retry on recoverable failures wastes the entire task
- Agent cannot distinguish "try again" from "fix your args first"

### Solutions

**`retryable` and `retry_after_ms` in every error:**
```json
{
  "ok": false,
  "error": {
    "code": "RATE_LIMITED",
    "message": "API rate limit exceeded",
    "retryable": true,
    "retry_after_ms": 5000,
    "retry_strategy": "exponential_backoff",
    "max_retries": 3
  }
}
```

```json
{
  "ok": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "retryable": false,
    "fix_required": "Correct the --email argument before retrying"
  }
}
```

**Retry classification taxonomy:**
```
retryable: false   → VALIDATION_ERROR, NOT_FOUND, PERMISSION_DENIED, CONFLICT
retryable: true    → TIMEOUT, SERVICE_UNAVAILABLE, RATE_LIMITED, NETWORK_ERROR
retryable: "maybe" → INTERNAL_ERROR (sometimes transient, sometimes not)
```

**Exit code alignment:**
```
Exit 9 (RATE_LIMITED)       → always retryable, check retry_after_ms
Exit 7 (TIMEOUT)            → retryable, immediate retry ok
Exit 8 (PERMISSION_DENIED)  → never retryable without auth change
Exit 2 (BAD_ARGS)           → never retryable without arg change
```

**For framework design:**
- Every error class has a default `retryable` value in the error registry
- `retry_after_ms` sourced from response header (Retry-After) when available
- Framework-level retry logic: honor `retryable` and `retry_after_ms` automatically
- Emit `attempt` and `max_attempts` in `meta` so agents know retry history
