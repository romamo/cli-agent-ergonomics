> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §42

## 42. Debug / Trace Mode Secret Leakage

**Severity:** Critical | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Low | **Time:** Low | **Context:** High

### The Problem

CLI frameworks often provide debug/trace modes that dump full invocation context to aid debugging. Python Fire's `--trace` flag prints the complete call trace including all argument values. Many tools have `--debug` or `--verbose` flags that log full request/response details. In agent contexts, these modes are dangerous because:

1. **Secrets in argument values are exposed verbatim**: An agent invokes `my-tool deploy --api-key sk-abc123` and adds `--trace`. The trace output includes `sk-abc123` in plaintext. If this trace is captured to logs or returned to the LLM context, the secret is exposed.

2. **Secrets in process tables**: Arguments passed as `--token <value>` appear in `process.argv` (Node.js), `sys.argv` (Python), and the system process table (`ps aux`). Any process with read access to `/proc/<pid>/cmdline` can extract the secret.

3. **Secrets in error messages**: Many frameworks echo back invalid argument values in error messages. `argparse` error for a bad `--api-url` value: `error: argument --api-url: invalid url value: 'http://secret-host/'`. If the "secret" is in a URL, it is now in stderr.

This is distinct from challenge #24 (Authentication & Secret Handling), which concerns the *storage* and *loading* of secrets (env vars, keychain, SecretStr). This challenge concerns the *leakage of secrets into diagnostic output* — traces, error messages, debug logs — that occurs after the secret has been successfully loaded.

```python
# Python Fire: --trace dumps everything
$ python my_fire_app.py deploy --api_key=sk-abc123 --region=us-east-1 -- --trace
Fire trace:
  1. Initial component
  2. ('deploy',): Called routine deploy(api_key='sk-abc123', region='us-east-1')
# api_key is now in plaintext in stdout
```

```bash
# Process table exposure
$ ps aux | grep my-tool
user 12345 ... my-tool deploy --api-key sk-abc123 --region us-east-1
# Secret visible to any user who can run ps
```

### Impact

- Secrets (API keys, tokens, passwords) exposed in debug output that may be captured by log collectors, audit systems, or LLM context.
- Process table exposure makes secrets visible to all users on the system during command execution.
- Error messages that echo back argument values can expose partial secrets.
- If the LLM context receives a trace with a secret, the secret may be included in future prompts, embeddings, or log entries.
- Particularly dangerous when agents run in shared infrastructure (CI/CD, multi-tenant environments).

### Solutions

**For CLI authors:**
```python
from pydantic import SecretStr

class DeployConfig(BaseModel):
    api_key: SecretStr  # repr never shows value; model_dump() returns "[REDACTED]"
    region: str

# Argparse: use action to mask value in namespace repr
import argparse
class SecretAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
    def __repr__(self):
        return f"{self.dest}=[REDACTED]"
```

**For framework design:**
- Apply name-based heuristics to automatically redact argument values whose names match `token|secret|password|key|credential|auth|apikey` in all trace/debug output.
- Never echo argument values in error messages for arguments marked `sensitive=True` or matching the redaction pattern.
- Provide a framework-level `--trace-safe` mode that produces a trace with sensitive fields replaced by `[REDACTED]`.
- For `--trace` or `--debug` modes: require explicit `--no-redact` opt-out to expose sensitive values.
- Use environment variables (not CLI flags) as the preferred injection mechanism for secrets — they are not visible in `process.argv` or process tables.
- Document in `--schema` output which arguments are marked sensitive: `"sensitive": true`.
