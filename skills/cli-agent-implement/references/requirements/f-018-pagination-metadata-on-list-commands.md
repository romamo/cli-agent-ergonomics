# REQ-F-018: Pagination Metadata on List Commands

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§5 Pagination & Large Output](../challenges/04-critical-output-and-parsing/05-high-pagination.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Critical

---

## Description

The framework MUST automatically inject a `pagination` object into the response envelope for every command declared as a list command. The `pagination` object MUST always contain: `total` (total count if known, or null), `returned` (count of items in this response), `truncated` (boolean), `has_more` (boolean), and `next_cursor` (opaque string token, or null if no more results). This metadata MUST be present even when the result is a complete set (with `truncated: false`).

## Acceptance Criteria

- Every list command response includes a `pagination` key at the top level of the envelope.
- When results are truncated, `truncated: true` and `next_cursor` is non-null.
- When results are complete, `truncated: false` and `next_cursor` is null.
- Passing `next_cursor` from response N as `--cursor` in the next call returns the subsequent page.
