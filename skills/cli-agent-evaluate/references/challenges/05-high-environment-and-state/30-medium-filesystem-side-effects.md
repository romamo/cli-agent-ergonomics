> **Part V: Environment & State** | Challenge §30

## 30. Undeclared Filesystem Side Effects

**Severity:** Medium | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Low | **Time:** Low | **Context:** Low

### The Problem

Tools write to locations the agent doesn't know about: caches, logs, lock files, temp dirs, credential stores. These accumulate silently, cause permission errors, leak data between sessions, and make behavior non-reproducible.

**Cache writes the agent can't control:**
```bash
$ tool fetch-schema --url https://api.example.com/schema
# Writes: ~/.cache/tool/schemas/api.example.com.json
# Agent doesn't know
# Next call: uses stale cache, returns wrong schema
# Agent has no way to invalidate or inspect the cache
```

**Log files accumulating without rotation:**
```bash
$ tool process large-file.csv
# Writes: ~/.local/share/tool/logs/2024-03-11.log (500MB)
# Agent runs 100 times: 50GB of logs
# Disk full → unrelated commands start failing
```

**Credential store side effects:**
```bash
$ tool login --token $TOKEN
# Writes: ~/.config/tool/credentials.json
# Another agent session overwrites same file with different token
# First session's subsequent calls now use wrong token
```

**Temp files that outlive the command:**
```bash
$ tool export --format xlsx
# Writes: /tmp/tool-export-abc123.xlsx
# Returns path in output
# Agent doesn't clean up → /tmp fills over time
```

### Impact

- Stale cache causes wrong results that are hard to trace
- Disk exhaustion from uncleaned logs/temp files
- Credential files stomped by concurrent sessions
- Data leaks: sensitive output persists on disk after session ends

### Solutions

**Declare all side effect locations in schema:**
```json
{
  "command": "fetch-schema",
  "filesystem_side_effects": [
    {
      "path": "~/.cache/tool/schemas/",
      "type": "cache",
      "ttl_seconds": 3600,
      "clearable_with": "tool cache clear --scope schemas"
    }
  ]
}
```

**`--no-cache` and `--cache-ttl` flags:**
```bash
tool fetch-schema --url ... --no-cache
tool fetch-schema --url ... --cache-ttl 0
```

**Temp files registered for cleanup:**
```json
{
  "ok": true,
  "data": {"path": "/tmp/tool-export-abc123.xlsx"},
  "cleanup": {
    "command": "tool cleanup --file /tmp/tool-export-abc123.xlsx",
    "auto_cleanup_after_seconds": 3600
  }
}
```

**`tool status --show-side-effects` inventory:**
```bash
$ tool status --show-side-effects --output json
{
  "cache": {"path": "~/.cache/tool/", "size_bytes": 45000000},
  "logs":  {"path": "~/.local/share/tool/logs/", "size_bytes": 524000000},
  "temp":  {"path": "/tmp/tool-*/", "count": 14, "size_bytes": 2000000}
}
```

**For framework design:**
- Every command declares `filesystem_side_effects` in its schema
- Framework provides `tool cleanup` that removes all known side effect paths
- Temp files use a session-scoped directory, auto-cleaned when session ends
- Log rotation built into framework (max size, max age)
