> **Part V: Environment & State** | Challenge §32

## 32. Self-Update & Auto-Upgrade Behavior

**Severity:** High | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Medium | **Time:** High | **Context:** Low

### The Problem

Some CLI tools automatically check for updates, download new versions, or silently upgrade themselves. For agents, this means behavior can change mid-session, schemas can shift, and version-pinned agent skills can break without warning.

**Silent auto-update on invocation:**
```bash
$ tool deploy
Updating tool to v2.1.0... done
Deployed successfully.

# Agent built against v1.x schema — v2.x changed output format
# Agent's JSON parsing now fails on future calls in the same session
# No indication that an update occurred in the JSON output
```

**Update check that delays execution:**
```bash
$ tool sync
Checking for updates...   [3 second pause]
No updates available.
Syncing...
# Every invocation: 3s wasted on update check
# Across 50 tool calls per agent session: 2.5 minutes wasted
```

**Update check that fails and crashes the tool:**
```bash
$ tool deploy
Error: failed to check for updates: connection refused to updates.example.com
exit 1
# Agent thinks deploy failed
# Actually: update check server is down, deploy never ran
```

**Background update that conflicts with running command:**
```bash
$ tool process large-file.csv
# Background updater overwrites tool binary mid-execution
# Process crashes with: "text file busy" or silent corruption
```

### Impact

- Schema changes mid-session break agent's output parsing
- Update check latency accumulates across all tool calls
- Update check failures masquerade as command failures
- Binary replacement during execution causes crashes

### Solutions

**Disable auto-update in non-interactive / CI contexts:**
```python
import sys, os

AUTO_UPDATE = (
    sys.stdin.isatty()
    and not os.environ.get("CI")
    and not os.environ.get("TOOL_NO_UPDATE")
)
```

**`--no-update-check` flag:**
```bash
tool deploy --no-update-check
# Skips update check entirely for this invocation
```

**Update check only on explicit command:**
```bash
tool update          # explicit: check and apply update
tool update --check  # check only, don't apply
# Never auto-update during other commands
```

**Include version in every response `meta`:**
```json
{
  "meta": {
    "tool_version": "1.4.2",
    "schema_version": "1.2.0",
    "update_available": "2.0.0",   // non-blocking: just informational
    "update_channel": "stable"
  }
}
```

**Never replace running binary:**
```bash
# Update writes to tool.new, renames on next cold start
# Never overwrites tool binary while any instance is running
```

**For framework design:**
- `TOOL_NO_UPDATE=1` env var disables all update behavior
- Auto-update disabled whenever `CI=true` or stdout is not a TTY
- Update available surfaced as `meta.update_available`, never blocks execution
- `tool update` is the only command that modifies the tool binary

---
