> **Part IV: Security** | Challenge §24

## 24. Authentication & Secret Handling

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

CLI tools often need credentials. How they receive, store, and expose those credentials determines whether agents can use them safely without leaking secrets into logs or context windows.

**Secrets in arguments (worst pattern):**
```bash
$ tool connect --password "supersecret"
# Appears in: ps aux, shell history, logs, agent context window
```

**Secrets in output:**
```bash
$ tool create-api-key --name "my-key"
API Key created: sk-prod-abc123xyz789
Store this somewhere safe, it won't be shown again.
# The secret is now in the agent's context window and any logs
```

**Secrets in error messages:**
```bash
$ tool connect --token $TOKEN
Error: Invalid token: "Bearer abc123xyz" — expected format: "Token sk-..."
# Token value echoed in error, ends up in logs
```

**Credential prompts in non-interactive mode:**
```bash
$ tool deploy
Enter API token:
# Hangs, or reads empty string, or fails with no explanation
```

### Impact

- Credentials exposed in agent context window → may be logged or transmitted
- Credentials in shell history → leaked via history files
- Credentials in error messages → leaked in log aggregation systems

### Solutions

**Prefer environment variables:**
```bash
TOOL_API_TOKEN=sk-... tool deploy
# Convention: TOOL_VARNAME
```

**Support secrets files:**
```bash
tool deploy --token-file /run/secrets/api-token
# File path, not the value
```

**Never echo secrets in output or errors:**
```json
// Bad
{"error": "Invalid token: sk-prod-abc123xyz789"}

// Good
{"error": {"code": "AUTH_TOKEN_INVALID", "message": "Token is invalid or expired"}}
```

**Secret output handling:**
```json
{
  "ok": true,
  "data": {
    "key_id": "key-42",          // safe to log
    "key_preview": "sk-prod-abc...xyz",  // truncated
    "secret": "REDACTED"          // never return in --output json
  },
  "secret_written_to": "/run/secrets/key-42"  // written to file instead
}
```

**For framework design:**
- Framework-level redaction: any field named `*token*`, `*secret*`, `*password*`, `*key*` is auto-redacted in logs
- Provide `--secret-from-env VAR_NAME` and `--secret-from-file PATH` as standard flags
- Document which env vars each command reads for credentials
