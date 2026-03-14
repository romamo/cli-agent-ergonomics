> **Part I: Output & Parsing** | Challenge §1

## 1. Exit Codes & Status Signaling

**Severity:** Critical | **Frequency:** Very Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Low

### The Problem

The most fundamental contract between a CLI tool and its caller is the exit code. Agents treat exit code `0` as success and anything else as failure — but many tools break this contract in ways that silently mislead the agent.

**Violations agents encounter constantly:**

```bash
# Tool exits 0 but operation failed
$ my-deploy --env prod
Warning: config file not found, using defaults
Deploying... timeout after 30s
$ echo $?
0   # ← agent thinks this succeeded
```

```bash
# Tool exits non-zero on non-error conditions
$ grep "pattern" file.txt
$ echo $?
1   # grep exits 1 when no match found — not an error, just "not found"
    # agent may treat this as a failure and retry or abort
```

```bash
# Inconsistent exit codes across versions
$ tool --version
v1.x: exit 0 on warning, exit 1 on error
v2.x: exit 2 on warning, exit 1 on error
# agent cannot reliably interpret without knowing version
```

**Multi-step commands that mask failures:**
```bash
cmd1 && cmd2 && cmd3
# if cmd2 fails, the shell exits with cmd2's code
# but the agent only sees the final code and doesn't know which step failed
```

### Impact

- Agent retries a succeeded operation (token waste, possible duplication)
- Agent proceeds after a failed operation (data corruption, cascading errors)
- Agent enters a retry loop on a "failure" that is actually expected behavior

### Solutions

**For CLI tool authors:**
```
Exit code conventions to follow:
  0  = success, operation completed as intended
  1  = general error (use sparingly — be specific)
  2  = misuse / bad arguments (before operation starts)
  3  = operation started but failed mid-way
  4  = precondition not met (dependency missing, not initialized)
  5  = not found (the thing you asked about doesn't exist)
  6  = conflict / already exists
  7  = timeout
  8  = permission denied
  9  = rate limited / quota exceeded
```

**Separate "not found" from "error":**
```bash
# Bad: exits 1 for both "error" and "not found"
tool get-user --id 123
# exit 1

# Good: exits 5 for "not found", 1 for actual errors
tool get-user --id 123
# exit 5  ← agent knows to stop, not retry
```

**For CLI framework design:**
- Define a standard exit code table in your framework
- Provide typed exit code constants (not magic numbers)
- Make every command document its possible exit codes in `--help`
- Support `--exit-on-warning` flag to make strict mode opt-in
