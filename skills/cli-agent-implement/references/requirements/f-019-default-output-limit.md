# REQ-F-019: Default Output Limit

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§5 Pagination & Large Output](../challenges/04-critical-output-and-parsing/05-high-pagination.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Critical

---

## Description

The framework MUST apply a default result limit of 20 items to every list command. This limit MUST be overridable by the caller using `--limit <n>`, and MUST be configurable per command by the author. An explicit `--limit 0` MUST disable the limit entirely (no implicit cap). The default limit MUST be documented in the command's schema output.

## Acceptance Criteria

- A list command invoked with no flags returns at most 20 items.
- `--limit 100` returns at most 100 items.
- `--limit 0` returns all available items.
- The default limit is visible in `tool <cmd> --schema`.

---

## Schema

**Types:** [`response-envelope.md`](../schemas/response-envelope.md)

When a default limit truncates results, the `pagination` object (from REQ-F-018) reflects this via `truncated: true` and `meta` carries no additional fields. The truncation state is fully expressed by `pagination.truncated` and `pagination.total`.

---

## Wire Format

Response where the default limit of 20 truncates a larger result set:

```json
{
  "ok": true,
  "data": [
    { "id": "item-1" },
    "...",
    { "id": "item-20" }
  ],
  "pagination": {
    "total": 150,
    "returned": 20,
    "truncated": true,
    "has_more": true,
    "next_cursor": "eyJsYXN0X2lkIjoiaXRlbS0yMCJ9"
  },
  "error": null,
  "warnings": [],
  "meta": {
    "request_id": "req_05GH",
    "command": "list-items",
    "timestamp": "2024-06-01T12:00:00Z"
  }
}
```

---

## Example

Framework-Automatic: no command author action needed. The framework applies `--limit 20` by default to all list commands.

```
$ tool list-items
→ 20 items returned, pagination.truncated: true, pagination.total: 150

$ tool list-items --limit 100
→ 100 items returned, pagination.truncated: true, pagination.total: 150

$ tool list-items --limit 0
→ 150 items returned, pagination.truncated: false, pagination.next_cursor: null

$ tool list-items --schema
→ flags: --limit (default: 20, 0 = unlimited)
```

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-018](f-018-pagination-metadata-on-list-commands.md) | F | Composes: pagination metadata reflects the limit applied by this requirement |
| [REQ-F-004](f-004-consistent-json-response-envelope.md) | F | Provides: response envelope that carries the truncated list |
| [REQ-C-015](c-015-commands-declare-input-and-output-schema.md) | C | Provides: schema output that exposes the default limit value |
