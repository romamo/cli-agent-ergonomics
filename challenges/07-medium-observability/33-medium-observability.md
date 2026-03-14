> **Part VI: Observability** | Challenge §33

## 33. Observability & Audit Trail

**Severity:** Medium | **Frequency:** Very Common | **Detectability:** Easy | **Token Spend:** Medium | **Time:** High | **Context:** Medium

### The Problem

When an agent-driven operation fails or produces unexpected results, there's often no way to trace what commands ran, in what order, with what parameters, and what they returned.

**No correlation between tool calls:**
```bash
# Three tool calls: deploy, verify, rollback
# Each has separate logs with no shared identifier
# Impossible to reconstruct the sequence after the fact
```

**No request ID in output:**
```bash
$ tool deploy
{"ok": true, "effect": "deployed"}
# No request ID to correlate with server-side logs
```

**No timing information:**
```bash
# Tool ran for 45 seconds
# Output has no timestamps
# Impossible to identify which step was slow
```

### Solutions

**Request/trace ID in every response:**
```json
{
  "ok": true,
  "meta": {
    "request_id": "req-abc123",
    "trace_id": "trace-xyz789",
    "duration_ms": 4521,
    "timestamp": "2024-03-11T14:30:00Z",
    "command": "deploy",
    "version": "1.2.3"
  }
}
```

**Correlation ID propagation:**
```bash
TOOL_TRACE_ID=agent-session-42-step-7 tool deploy
# All log entries for this call include the trace ID
```

**Structured audit log:**
```bash
$ tool audit-log --since 1h --output jsonl
{"timestamp": "...", "command": "deploy", "params": {...},
 "exit_code": 0, "duration_ms": 4521, "operator": "agent-session-42"}
```

**For framework design:**
- Every response includes `meta.request_id` (server-assigned) and `meta.trace_id` (caller-supplied)
- `TOOL_TRACE_ID` env var propagated automatically
- Framework writes append-only audit log to `~/.local/share/tool/audit.jsonl`

---
