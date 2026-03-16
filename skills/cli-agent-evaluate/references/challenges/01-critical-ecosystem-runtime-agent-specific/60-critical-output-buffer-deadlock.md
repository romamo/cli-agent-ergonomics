> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §60

## 60. OS Output Buffer Deadlock

**Source:** Antigravity `01_io_and_formatting.md` (RA)

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Critical | **Context:** Low

### The Problem

When a CLI tool's stdout is connected to a pipe rather than a TTY, the OS switches from line-buffered to fully-buffered mode (typically 4KB or 8KB blocks). A tool that emits incremental progress logs one line at a time appears completely silent to the agent — output accumulates in the kernel buffer and is released only when the buffer fills or the process exits. The agent sees no output for minutes, then receives everything at once (or nothing if the tool crashes mid-way and the buffer is lost).

```bash
# Tool emits one log line per second to stdout:
$ my-tool migrate --env prod | agent-receiver
# Agent sees... nothing for 4 minutes
# Then receives all 240 log lines simultaneously when buffer flushes
# Agent cannot tell: is the tool running? stuck? crashed?

# The OS buffer behavior is invisible to both the tool and the agent:
$ strace -e write my-tool migrate 2>/dev/null
write(1, "Step 1/10: validating...\n", 25) = 25  # buffered by OS, not sent yet
write(1, "Step 2/10: connecting...\n", 25) = 25   # still buffered
# ...240 more writes... buffer fills at 4KB → flush → agent receives everything
```

This is the **pipe buffering problem**: standard C library `stdio` and Python's `sys.stdout` switch to block-buffered mode when output is not a TTY.

### Impact

- Agent receives no output for the entire duration of a long-running command
- No heartbeat, no progress — agent cannot distinguish "running" from "hung"
- Agent's timeout fires before buffer flushes; all output lost
- Error output (if on stdout) arrives only at the end, too late for the agent to react

### Solutions

**Unbuffer stdout explicitly in non-TTY mode:**
```python
# Python: disable buffering
import sys, os
if not sys.stdout.isatty():
    sys.stdout.reconfigure(line_buffering=True)
    # or: os.environ['PYTHONUNBUFFERED'] = '1'
```

```bash
# Wrapper: force unbuffered output
$ stdbuf -o0 my-tool migrate
$ unbuffer my-tool migrate   # via expect package
```

**Emit JSON heartbeats every N seconds for long operations:**
```json
{"status": "running", "step": "migrating table users", "elapsed_ms": 5000, "heartbeat": true}
```

**For framework design:**
- Framework MUST call `sys.stdout.reconfigure(line_buffering=True)` (Python) or `setvbuf(stdout, NULL, _IOLBF, 0)` (C) on startup when stdout is not a TTY.
- Long-running commands MUST emit a JSON heartbeat object to stdout every configurable interval (default: 10s) so the agent has proof of life.
- `PYTHONUNBUFFERED=1` and equivalent env vars MUST be set in the framework's bootstrap before any output.
