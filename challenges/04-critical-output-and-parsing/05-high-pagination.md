> **Part I: Output & Parsing** | Challenge §5

## 5. Pagination & Large Output

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Critical

### The Problem

Commands that return large datasets in a single response create multiple problems: the output may be too large to parse, may exceed pipe buffers, or may contain more data than the agent can process in its context.

**Unbounded output:**
```bash
$ tool list-logs
[returns 50,000 lines of JSON]
# Pipe buffer overflows, agent context overflows, parsing degrades
```

**No indication that results are truncated:**
```bash
$ tool list-users
{"users": [...100 items...]}
# Is this all users? Or first 100? Agent can't tell.
```

**Pagination that requires stateful session:**
```bash
$ tool list-users --page 2
# Requires knowing that page 1 was fetched first
# No cursor-based alternative
```

### Solutions

**Always indicate truncation and total:**
```json
{
  "ok": true,
  "data": [...],
  "pagination": {
    "total": 50000,
    "returned": 100,
    "truncated": true,
    "next_cursor": "eyJpZCI6MTAwfQ==",
    "has_more": true
  }
}
```

**Cursor-based pagination (stateless):**
```bash
tool list-users --limit 100 --cursor "eyJpZCI6MTAwfQ=="
```

**Streaming output (JSONL):**
```bash
tool list-logs --output jsonl --stream
# Emits one JSON object per line
# Agent can process incrementally
{"timestamp": "...", "level": "error", "message": "..."}
{"timestamp": "...", "level": "info",  "message": "..."}
```

**Default sensible limits:**
```bash
tool list-users           # default: --limit 20
tool list-users --limit 0 # explicit: no limit
```

**For framework design:**
- All list commands have `--limit` (default: 20) and `--cursor`
- Response always includes `pagination` metadata
- `--stream` flag for JSONL output when processing large sets
