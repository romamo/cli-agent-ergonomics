> **Part II: Execution & Reliability** | Challenge §16

## 16. Signal Handling & Graceful Cancellation

**Severity:** High | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

Agents enforce time budgets by killing processes (SIGTERM, then SIGKILL). Most CLI tools handle this by dying instantly — no cleanup, no output, no indication of what state was left behind.

**Default signal behavior (the bad path):**
```bash
$ tool migrate-database &
PID=1234

# Agent times out, kills the process:
$ kill -TERM 1234

# Tool dies immediately:
# - No output emitted
# - Temp files left on disk
# - Lock file not released
# - Database partially migrated
# - Agent receives: exit code 143 (128+SIGTERM), empty stdout
```

**SIGPIPE on broken pipe:**
```bash
$ tool list-logs | head -5
# After head exits, tool receives SIGPIPE
# Default: Python raises BrokenPipeError → ugly traceback to stderr
# Default: Go panics or silently exits non-zero
# Agent sees an error that isn't really an error
```

**No grace period between SIGTERM and SIGKILL:**
```bash
# Agent sends SIGTERM, waits 0ms, sends SIGKILL
# Tool had no chance to write partial results or clean up
```

### Impact

- Unknown intermediate state after cancellation
- Lock files and temp files accumulate, causing failures on next run
- Agent gets no information about what was completed before kill
- SIGPIPE masquerades as error, causing unnecessary retries

### Solutions

**Register signal handlers that emit JSON then exit cleanly:**
```python
import signal, sys, json, atexit

_cleanup_done = False

def handle_sigterm(signum, frame):
    global _cleanup_done
    if _cleanup_done:
        return
    _cleanup_done = True
    # Emit partial result to stdout before exit
    result = {
        "ok": False,
        "partial": True,
        "error": {"code": "CANCELLED", "message": "Process received SIGTERM"},
        "completed_steps": get_completed_steps(),
        "resume_from": get_current_step()
    }
    sys.stdout.write(json.dumps(result) + "\n")
    sys.stdout.flush()
    cleanup_temp_files()
    release_locks()
    sys.exit(143)  # 128 + SIGTERM

signal.signal(signal.SIGTERM, handle_sigterm)
atexit.register(cleanup_temp_files)
```

**SIGPIPE handling:**
```python
# Python: suppress BrokenPipeError on stdout
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
# or wrap all stdout writes in try/except BrokenPipeError
```

**Advertise cancellation support in schema:**
```json
{
  "command": "migrate-database",
  "cancellable": true,
  "cancel_signal": "SIGTERM",
  "cancel_grace_period_ms": 5000,
  "on_cancel": "emits partial result + rollback available"
}
```

**For framework design:**
- Framework installs SIGTERM and SIGPIPE handlers automatically for every command
- Every command declares a `cleanup()` hook called on signal
- Grace period: framework sends SIGTERM, waits `cancel_grace_period_ms`, then SIGKILL
- Partial result always emitted to stdout before exit, even on cancellation
