> **Part IV: Security** | Challenge §23

## 23. Side Effects & Destructive Operations

**Severity:** Critical | **Frequency:** Common | **Detectability:** Medium | **Token Spend:** Medium | **Time:** High | **Context:** Medium

### The Problem

Agents may execute destructive commands without fully understanding consequences, especially when operating autonomously or when command names are ambiguous.

**Ambiguous destructive commands:**
```bash
$ tool clean          # Does it clean temp files? Or delete all data?
$ tool reset          # Reset config? Or wipe the database?
$ tool update         # Update records? Update the tool itself?
$ tool sync --force   # What does force do exactly?
```

**No indication of destructive nature:**
```bash
$ tool deploy --env prod --strategy rolling
# Starts replacing production instances
# No warning, no confirmation, no dry-run output
```

**Irreversible operations without warning:**
```bash
$ tool delete-account --user 42
Deleted.
# No warning that this is permanent, no audit log, no --dry-run available
```

### Impact

- Agent causes unintended data loss in production
- No recovery path after irreversible operation
- Hard to audit what happened and when

### Solutions

**Explicit destructive flag:**
```bash
tool delete-account --user 42 --confirm-destructive
# Without the flag: exits with clear error explaining the flag is required
```

**Machine-readable danger level in help:**
```json
{
  "command": "delete-account",
  "danger_level": "destructive",   // "safe" | "mutating" | "destructive"
  "reversible": false,
  "requires_confirmation": true
}
```

**Dry-run always available for destructive commands:**
```bash
$ tool delete-account --user 42 --dry-run
{
  "ok": true,
  "effect": "would_delete",
  "would_affect": {
    "user": {"id": 42, "name": "Alice"},
    "related_records": 234,
    "reversible": false
  }
}
```

**Audit output:**
```json
{
  "ok": true,
  "effect": "deleted",
  "audit": {
    "timestamp": "2024-03-11T14:30:00Z",
    "operator": "agent-session-abc123",
    "target": {"type": "user", "id": 42},
    "reversible": false
  }
}
```

**For framework design:**
- Commands declare `danger_level` in their schema
- Framework enforces `--dry-run` availability for all `destructive` commands
- `--yes` / `--confirm-destructive` flags auto-supplied by agent harness
- Generate audit log entries for all `mutating` and `destructive` operations
