# REQ-F-064: Output Truncation Detection and Warning

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§55 Silent Data Truncation](../challenges/01-critical-ecosystem-runtime-agent-specific/55-high-silent-truncation.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST detect and report data truncation rather than silently returning a truncated value. When a field value is truncated (by a backend API, database column limit, or framework response size cap from REQ-F-052), the framework MUST: set `meta.truncated: true` in the response, include a `TRUNCATION` entry in `warnings[]` with the field path and byte counts (`original_bytes` if known, `returned_bytes`), and ensure the truncated value is clearly terminated (e.g., appended with a truncation marker). Commands that write to size-limited fields MUST declare `max_bytes: N` per field in their schema; the framework validates write payloads against these limits before submission and exits 2 if exceeded.

## Acceptance Criteria

- Writing a 500-byte value to a field declared `max_bytes: 255` exits 2 with a structured error before writing.
- Reading a pre-truncated value from a backend produces `meta.truncated: true` and a `TRUNCATION` warning.
- The warning includes `field`, `returned_bytes`, and (where known) `original_bytes`.
- `json.loads(stdout)` succeeds even when truncation is present — the response envelope is always complete.
