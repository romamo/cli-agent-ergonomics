> **Part II: Execution & Reliability** | Challenge §13

## 13. Partial Failure & Atomicity

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Medium

### The Problem

Multi-step commands can fail mid-execution, leaving the system in an unknown intermediate state. The agent receives a failure but doesn't know what was completed.

**Partial failure with no rollback:**
```bash
$ tool migrate-database
Step 1/4: backup... done
Step 2/4: apply schema changes... done
Step 3/4: migrate data... FAILED (disk full)
Step 4/4: (not reached)
exit 1
```
Agent retries. Step 2 runs again. Now schema is applied twice → error.

**Batch operations with partial success:**
```bash
$ tool send-notifications --users 1,2,3,4,5
Sent to user 1: ok
Sent to user 2: ok
Sent to user 3: FAILED (invalid email)
Sent to user 4: ok
Sent to user 5: FAILED (rate limited)
exit 1
```
Exit code 1 tells agent "failed" but 3/5 succeeded. Retry sends duplicates to 1, 2, 4.

### Impact

- Retry causes double execution of already-completed steps
- Agent cannot determine safe recovery path
- Manual intervention required to resolve unknown state

### Solutions

**Structured partial failure output:**
```json
{
  "ok": false,
  "partial": true,
  "completed_steps": ["backup", "apply_schema"],
  "failed_step": "migrate_data",
  "error": {"code": "DISK_FULL", "message": "..."},
  "resume_from": "migrate_data",
  "rollback_available": true
}
```

**Batch result per item:**
```json
{
  "ok": false,
  "partial": true,
  "results": [
    {"id": 1, "ok": true,  "effect": "sent"},
    {"id": 2, "ok": true,  "effect": "sent"},
    {"id": 3, "ok": false, "error": {"code": "INVALID_EMAIL"}},
    {"id": 4, "ok": true,  "effect": "sent"},
    {"id": 5, "ok": false, "error": {"code": "RATE_LIMITED"}}
  ],
  "summary": {"total": 5, "succeeded": 3, "failed": 2}
}
```

**Resumable commands:**
```bash
tool migrate-database --resume-from migrate_data
# Only runs remaining steps
```

**For framework design:**
- All multi-step commands emit a step manifest at start
- Each step emits its result as it completes (streaming JSON lines)
- Final summary always includes `completed`, `failed`, `skipped` counts
- `--rollback-on-failure` flag as standard option
