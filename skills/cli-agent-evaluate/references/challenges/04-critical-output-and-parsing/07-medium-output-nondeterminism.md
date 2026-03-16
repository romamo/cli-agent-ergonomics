> **Part I: Output & Parsing** | Challenge §7

## 7. Output Non-Determinism

**Severity:** Medium | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

Agents compare outputs, cache results, detect changes, and build logic on top of command results. If the same command with the same arguments produces different output on successive runs, all of these break silently.

**Random map/set ordering:**
```bash
$ tool list-permissions --role admin
{"permissions": ["write", "read", "delete", "admin"]}

$ tool list-permissions --role admin
{"permissions": ["admin", "delete", "read", "write"]}

# Agent compares: permissions changed? No — just reordered.
# Diff-based change detection: false positive every time
```

**Timestamps embedded in data fields:**
```bash
$ tool get-status --output json
{"status": "ok", "checked_at": "2024-03-11T14:30:01Z", "uptime": 3600}

$ tool get-status --output json
{"status": "ok", "checked_at": "2024-03-11T14:30:04Z", "uptime": 3603}

# Agent caches result, checks if output changed: always "changed"
# Retry detection: can't tell if operation ran twice or output just differs
```

**Random IDs in dry-run output:**
```bash
$ tool deploy --dry-run
{"effect": "would_create", "preview_id": "prev-a3f2c1"}

$ tool deploy --dry-run
{"effect": "would_create", "preview_id": "prev-9b4d2e"}

# Agent uses preview_id for follow-up call: ID is already stale
```

**Unordered batch results:**
```bash
$ tool list-users
{"users": [{"id": 3}, {"id": 1}, {"id": 2}]}  # run 1

$ tool list-users
{"users": [{"id": 1}, {"id": 3}, {"id": 2}]}  # run 2 — different order
```

### Impact

- Change detection produces constant false positives
- Result caching is impossible
- Agent cannot tell "operation ran twice" from "output varies naturally"
- Dry-run IDs are unusable for follow-up calls

### Solutions

**Sort all collections in output:**
```json
// Always sort arrays of objects by a stable key
{"users": [{"id": 1}, {"id": 2}, {"id": 3}]}

// Always sort string arrays lexicographically
{"permissions": ["admin", "delete", "read", "write"]}
```

**Separate volatile metadata from stable data:**
```json
{
  "ok": true,
  "data": {                          // stable — safe to cache/compare
    "status": "ok",
    "version": "1.2.3"
  },
  "meta": {                          // volatile — do not compare
    "checked_at": "2024-03-11T14:30:01Z",
    "duration_ms": 45,
    "request_id": "req-abc"
  }
}
```

**Deterministic dry-run IDs:**
```bash
# Dry-run preview ID derived from inputs, not random
preview_id = sha256(command + args + timestamp_truncated_to_minute)
# Same args within the same minute → same preview ID
```

**`--stable-output` flag:**
```bash
tool list-users --stable-output
# Sorts all collections, omits volatile fields (timestamps, durations)
# Output is deterministic for identical inputs
```

**For framework design:**
- All array fields sorted by default in `--output json` mode
- `data` and `meta` are top-level siblings; agents compare `data` only
- Dry-run IDs are content-addressed, not random
- Document which fields are volatile in the output schema (`"volatile": true`)
