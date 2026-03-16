> **Part II: Execution & Reliability** | Challenge §17

## 17. Child Process Leakage

**Severity:** Medium | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Low | **Time:** Low | **Context:** Low

### The Problem

CLI tools frequently spawn background processes — log forwarders, file watchers, health monitors, connection pools. When the main CLI process exits, these children are often orphaned, accumulating over time and consuming resources.

**Orphaned children from normal exit:**
```bash
$ tool start-watcher --dir /project
# Spawns: inotify daemon (PID 5678)
# Main process exits: 0
# inotify daemon: still running, never cleaned up

# After 100 agent calls: 100 inotify daemons running
```

**Children that hold locks:**
```bash
$ tool sync
# Spawns background sync process that holds /var/lock/tool.lock
# Main process exits
# Lock never released
# Next `tool sync` call: "Error: lock held by PID 5678 (defunct)"
```

**Children that write to stdout after parent exits:**
```bash
$ tool deploy
# Spawns background health-check process
# Main process exits, prints JSON result
# 2 seconds later: background process prints "health: ok" to stdout
# Agent's JSON parse of captured output now fails (extra text after valid JSON)
```

**Signal not forwarded to children:**
```bash
$ kill -TERM $TOOL_PID
# Tool exits cleanly
# But spawned children never received SIGTERM
# They run forever as orphans owned by init/PID1
```

### Impact

- Resource exhaustion: file descriptors, memory, CPU from accumulated orphans
- Lock files held by dead-parent children block all future invocations
- Stdout corruption from children writing after parent exits
- Containers/VMs accumulate ghost processes that survive restarts

### Solutions

**Process group management:**
```python
import os, signal, atexit

# Start child in its own process group
child = subprocess.Popen(
    ["child-process"],
    start_new_session=True,   # new process group
    preexec_fn=os.setsid
)

# On exit, kill the entire process group
def cleanup():
    try:
        os.killpg(os.getpgid(child.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass  # already dead

atexit.register(cleanup)
signal.signal(signal.SIGTERM, lambda *_: (cleanup(), sys.exit(143)))
```

**PID file tracking:**
```bash
$ tool start-watcher --dir /project
# Writes child PIDs to: /tmp/tool-session-42/children.pids
# Provides cleanup command:
{
  "ok": true,
  "background_pid": 5678,
  "cleanup_command": "tool stop-watcher --session 42",
  "pid_file": "/tmp/tool-session-42/children.pids"
}
```

**Mandatory child tracking in schema:**
```json
{
  "command": "start-watcher",
  "spawns_background_process": true,
  "cleanup_command": "stop-watcher",
  "max_lifetime_seconds": 3600
}
```

**Stdout close before spawning detached children:**
```python
# If spawning a truly detached daemon:
# 1. Complete all stdout writes and flush
# 2. Close stdout
# 3. Only then fork the background process
sys.stdout.flush()
sys.stdout.close()
child = subprocess.Popen(["daemon"], close_fds=True, stdin=DEVNULL,
                          stdout=DEVNULL, stderr=DEVNULL)
```

**For framework design:**
- Framework tracks all child PIDs in a session file automatically
- `tool session cleanup --id $SESSION` kills all tracked children
- Commands that spawn background processes must declare `spawns_background_process: true`
- Framework installs a SIGTERM handler that forwards to all tracked children before exit

---
