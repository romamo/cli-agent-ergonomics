> **Part III: Errors & Discoverability** | Challenge §22

## 22. Schema Versioning & Output Stability

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Medium

### The Problem

Agents built against a tool's output schema break silently when that schema changes. A field renamed, a type changed, or a new required field added can corrupt downstream logic with no warning.

**Silent breaking change:**
```bash
# Tool v1.x:
$ tool get-user --id 42
{"id": 42, "name": "Alice", "email": "alice@example.com"}

# Tool v2.x (field renamed):
$ tool get-user --id 42
{"id": 42, "full_name": "Alice", "email_address": "alice@example.com"}

# Agent code: user["name"]  → KeyError, silent None, or wrong value
# Agent was never told the schema changed
```

**Type change without notice:**
```bash
# v1: "status" was a string
{"status": "active"}

# v2: "status" is now an object
{"status": {"value": "active", "since": "2024-01-01"}}

# Agent: if result["status"] == "active" → always False now
```

**New required output field breaks agent parsing:**
```bash
# Agent extracts specific fields; new mandatory fields are ignored
# But if agent does strict schema validation, it rejects the response
```

### Impact

- Silent wrong behavior (agent reads stale field, gets None/wrong value)
- Hard to debug: agent works fine until tool is upgraded
- No way to detect the mismatch without version checking

### Solutions

**Schema version in every response:**
```json
{
  "ok": true,
  "meta": {
    "schema_version": "2.1.0",
    "tool_version": "2.4.1"
  },
  "data": {...}
}
```

**Deprecation warnings before removal:**
```json
{
  "ok": true,
  "data": {
    "name": "Alice",        // deprecated, use full_name
    "full_name": "Alice"    // new field
  },
  "warnings": [
    {
      "code": "FIELD_DEPRECATED",
      "message": "Field 'name' is deprecated. Use 'full_name' instead.",
      "removed_in": "3.0.0"
    }
  ]
}
```

**Stability tiers declared in schema:**
```json
{
  "fields": {
    "id":         {"stability": "stable"},
    "full_name":  {"stability": "stable"},
    "score":      {"stability": "experimental", "may_change": true},
    "_internal":  {"stability": "private", "do_not_depend_on": true}
  }
}
```

**Version negotiation:**
```bash
tool get-user --id 42 --schema-version 1
# Returns v1-compatible output even from v2 tool
# Allows gradual migration
```

**For framework design:**
- `meta.schema_version` in every response (semver)
- `--schema-version` flag to request compatible output
- Deprecation warnings 2 major versions before removal
- `tool changelog --output json` lists all schema changes by version

---
