> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §58

## 58. Multi-Agent Concurrent Invocation Conflict

**Severity:** High | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Medium | **Time:** High | **Context:** Low

### The Problem

Distinct from §15 (race conditions within a single invocation), this is about multiple independent agent instances invoking the same CLI tool simultaneously against shared state: config files, credential caches, state databases. Neither agent knows about the other. Both read-modify-write the same config file, resulting in last-writer-wins corruption with no error reported.

```bash
# Agent A and Agent B run simultaneously:
# Agent A: tool config set region=us-east-1
# Agent B: tool config set environment=staging
# Both read config.json, write their change; last write overwrites the other.
# Both exit 0. Both think they succeeded. Config is corrupted.

# Auth token cache:
# Agent A refreshes token → old token invalidated
# Agent B still holds old token → all B's calls start failing with 401
```

### Impact

- Silent config corruption — both agents exit 0 but state is wrong
- Auth invalidation cascade — token refresh by one agent breaks all others
- No signal of the conflict; failure surfaces much later

### Solutions

**File locking for all config writes:**
```python
with framework.config_lock(timeout_ms=5000) as lock:
    config = lock.read()
    config['region'] = 'us-east-1'
    lock.write(config)
# If lock times out: exit 6 (conflict) with error.code: "CONCURRENT_MODIFICATION"
```

**Per-agent-instance state namespacing:**
```bash
$ tool --instance-id agent-1 config set region=us-east-1
# Writes to ~/.tool/instances/agent-1/config.json
```

**For framework design:**
- All config and state writes MUST use advisory file locking with configurable timeout (default 5s).
- Config writes MUST use atomic rename to prevent partial-write corruption.
- Framework MUST provide `--instance-id <id>` to namespace all per-instance state so parallel agents operate without interference.
