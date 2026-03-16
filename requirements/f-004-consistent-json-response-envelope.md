# REQ-F-004: Consistent JSON Response Envelope

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§2 Output Format & Parseability](../challenges/04-critical-output-and-parsing/02-critical-output-format.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Medium / Context: High

---

## Description

The framework MUST wrap all command output in a standard JSON envelope. The envelope MUST always contain: `ok` (boolean), `data` (the command's primary output — present even when null or empty array), `error` (null on success, structured object on failure), `warnings` (array, may be empty), and `meta` (object with framework-populated fields). The schema of this envelope MUST NOT vary based on result count, command type, or success/failure state — the same top-level keys MUST always be present.

## Acceptance Criteria

- A JSON schema validator for the envelope passes on every command's stdout output in JSON mode.
- `data` key is present and non-absent on both success and failure responses.
- `error` key is present on all responses (null on success, structured object on failure).
- Single-result and multi-result commands produce structurally identical envelopes.

---

## Schema

**Types:** [`response-envelope.md`](../schemas/response-envelope.md)
