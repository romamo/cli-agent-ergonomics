> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §55

## 55. Silent Data Truncation

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

CLI tools that write to remote APIs often silently truncate field values that exceed API limits: descriptions > 255 chars, names > 64 chars, tag arrays > 10 items. The tool reports `exit 0` and `"ok": true`, but the resource was created with silently truncated data. The agent has no way to know the intended values weren't fully stored.

```bash
$ tool create-issue \
  --title "This is a very long title that definitely exceeds the 64 character limit"

{"ok": true, "data": {"id": 123, "title": "This is a very long title that definitely"}}
# Exit 0. Title was truncated silently. Agent proceeds with wrong assumption.
```

Array truncation is worse — items are silently dropped:
```bash
$ tool tag-resource --id res_1 --tags a,b,c,d,e,f,g,h,i,j,k  # 11 tags, limit is 10
# k was dropped. Agent thinks all 11 tags were applied.
```

### Impact

- Data integrity violations completely invisible to the agent at operation time
- Agent reasoning built on "confirmed" values that were actually altered
- Downstream operations reference data that doesn't exist as expected

### Solutions

**Truncated fields MUST appear in `warnings[]`:**
```json
{
  "ok": true,
  "warnings": [
    {
      "code": "FIELD_TRUNCATED",
      "field": "title",
      "original_length": 71,
      "truncated_to": 41
    }
  ]
}
```

**Better: reject at Phase 1 validation with field constraints from schema:**
```json
{ "name": "title", "type": "string", "max_length": 64 }
{ "name": "tags",  "type": "array",  "max_items": 10 }
```

**For framework design:**
- Schema MUST declare `max_length`, `max_items`, `max_bytes` for all bounded fields; Phase 1 rejects inputs exceeding these limits.
- If backend silently truncates anyway, framework MUST compare returned vs sent value and inject `FIELD_TRUNCATED` warning automatically.
