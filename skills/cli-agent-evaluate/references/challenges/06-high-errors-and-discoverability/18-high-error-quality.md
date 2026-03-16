> **Part III: Errors & Discoverability** | Challenge §18

## 18. Error Message Quality

**Severity:** High | **Frequency:** Very Common | **Detectability:** Easy | **Token Spend:** High | **Time:** Medium | **Context:** High

### The Problem

When a command fails, the agent needs to understand: what failed, why, and what to do next. Vague, undirected, or human-only error messages force the agent to guess.

**Errors that don't help the agent:**
```bash
$ tool deploy
Error: Something went wrong
exit 1
# Agent has zero actionable information
```

```bash
$ tool connect --host db.example.com
Connection failed.
exit 1
# Was it DNS? Auth? Firewall? Timeout? Agent doesn't know which to fix.
```

```bash
$ tool validate config.yaml
Validation error on line 14
exit 1
# Agent doesn't know what the error is, what the fix is, or what field
```

**Stack traces as error output:**
```bash
$ tool process file.csv
Traceback (most recent call last):
  File "tool.py", line 234, in process
    result = parser.parse(row)
  File "tool.py", line 89, in parse
    return int(row['count'])
ValueError: invalid literal for int() with base 10: 'N/A'
exit 1
# Agent receives a Python traceback — high token cost, low actionability
```

**Errors that require human interpretation:**
```bash
$ tool sync
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '42' for key 'PRIMARY'
exit 1
# Agent would need to reason about SQL error codes
```

### Impact

- Agent retries with identical parameters (no basis to change anything)
- Agent escalates to user with no useful information
- Token waste reasoning about unparseable error text

### Solutions

**Structured error format:**
```json
{
  "ok": false,
  "error": {
    "code": "CONNECTION_REFUSED",      // machine-readable code
    "message": "Cannot connect to database at db.example.com:5432",
    "cause": "Connection refused (ECONNREFUSED)",
    "suggestion": "Verify the database is running: `tool db status`",
    "docs_url": "https://docs.example.com/errors/CONNECTION_REFUSED",
    "context": {
      "host": "db.example.com",
      "port": 5432,
      "timeout_ms": 5000
    }
  }
}
```

**Error code taxonomy:**
```
{DOMAIN}_{NOUN}_{CONDITION}

Examples:
  DB_CONNECTION_REFUSED
  AUTH_TOKEN_EXPIRED
  FILE_CONFIG_NOT_FOUND
  API_RATE_LIMIT_EXCEEDED
  INPUT_PARAM_INVALID
```

**Suggestion field for common errors:**
```json
"suggestion": "Run `tool login` to refresh your credentials"
"suggestion": "Use --force to overwrite existing file"
"suggestion": "Check network connectivity with: ping db.example.com"
```

**For framework design:**
- All errors MUST have a `code` (machine) and `message` (human)
- `suggestion` field is encouraged for recoverable errors
- Never emit raw stack traces to stdout; log them to stderr or a file
- Provide an error code registry queryable via `tool errors list`
