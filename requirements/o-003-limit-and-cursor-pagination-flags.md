# REQ-O-003: --limit and --cursor Pagination Flags

**Tier:** Opt-In | **Priority:** P0

**Source:** [§5 Pagination & Large Output](../challenges/04-critical-output-and-parsing/05-high-pagination.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Critical

---

## Description

The framework MUST register `--limit <n>` and `--cursor <token>` as standard flags on all list commands. `--limit` controls maximum items returned. `--cursor` accepts an opaque pagination token from the previous response's `pagination.next_cursor`. The cursor MUST be stateless (self-contained, not dependent on server-side session). The framework MUST reject `--cursor` values that are expired or invalid with a structured error.

## Acceptance Criteria

- `--limit 50` returns at most 50 items.
- Passing `pagination.next_cursor` from response N as `--cursor` returns the next page.
- An invalid `--cursor` value returns a structured error, not a crash.
- Cursor tokens are URL-safe strings (base64url or similar encoding).
