# REQ-F-005: Locale-Invariant Serialization

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§2 Output Format & Parseability](../challenges/04-critical-output-and-parsing/02-critical-output-format.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Medium / Context: High

---

## Description

The framework's JSON serializer MUST always use invariant formatting: period (`.`) as decimal separator, no thousands separator, ISO 8601 format for all dates and datetimes (e.g., `2024-03-11T14:30:00Z`), JSON `true`/`false` for booleans (never `yes`/`no`/`1`/`0`). The serializer MUST NOT be influenced by the `LC_*` or `LANG` environment variables.

## Acceptance Criteria

- Output produced on a `de_DE` locale system is byte-for-byte identical to output on an `en_US` system for the same inputs.
- All date fields in output match the regex `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}`.
- Numeric fields in output contain no comma thousands separators.
- Boolean fields in output are exactly `true` or `false`.
