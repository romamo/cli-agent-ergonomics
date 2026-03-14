> **Part II: Execution & Reliability** | Challenge §15

## 15. Race Conditions & Concurrency

**Severity:** High | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

Agents may invoke multiple tool calls in parallel. CLI tools designed for single-user sequential use can corrupt shared state when called concurrently.

**Lock file conflicts:**
```bash
# Two parallel agent tool calls:
$ tool build   # writes to /tmp/tool.lock
$ tool test    # also writes to /tmp/tool.lock → conflict

# One gets: Error: lock file exists
# Other: runs fine
# Agent doesn't know which one to retry
```

**Shared temp files:**
```bash
$ tool process --input data.csv --output /tmp/result.json
# Two parallel calls both write to /tmp/result.json
# One overwrites the other's result silently
```

**Race on config mutation:**
```bash
# Parallel calls:
$ tool config set key1 val1   # reads config, writes key1
$ tool config set key2 val2   # reads config (before key1 written), writes key2
# Result: key1 is lost
```

### Solutions

**Session-isolated temp paths:**
```bash
tool process --input data.csv --session-id $AGENT_SESSION_ID
# Uses /tmp/tool/$AGENT_SESSION_ID/result.json automatically
```

**Advisory locking with timeout:**
```bash
$ tool build
Error: {
  "code": "LOCK_HELD",
  "message": "Another build is running (pid 1234, started 30s ago)",
  "suggestion": "Wait for it to complete or use --force-unlock if process is dead",
  "retry_after_ms": 5000
}
```

**For framework design:**
- All temp files scoped to `$TOOL_SESSION_ID` or a random run ID
- Lock acquisition has a timeout and emits `retry_after_ms`
- Config mutations use atomic write (write to temp, rename)
