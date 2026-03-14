# REQ-C-013: Error Responses Include Code and Message

**Tier:** Command Contract | **Priority:** P0

**Source:** [§18 Error Message Quality](../challenges/06-high-errors-and-discoverability/18-high-error-quality.md)

**Addresses:** Severity: High / Token Spend: High / Time: Medium / Context: High

---

## Description

Every error response MUST include an `error` object with: `code` (string, `DOMAIN_NOUN_CONDITION` format, machine-readable), `message` (string, human-readable, complete sentence), and optionally `cause` (the underlying system error), `suggestion` (an actionable next step), `docs_url` (a URL to documentation), and `context` (an object of relevant key-value pairs). Stack traces MUST NOT appear in `error.message` or any stdout field; they MUST be sent only to stderr or a log file.

## Acceptance Criteria

- Every non-zero exit code response includes a non-null `error` object.
- `error.code` matches the pattern `[A-Z][A-Z0-9_]+`.
- `error.message` is a complete human-readable sentence.
- No stack trace text appears anywhere in stdout output.
- `error.suggestion` is present for all errors the command author classifies as recoverable.

---

## Schema

**Types:** [`exit-code.json`](../schemas/exit-code.json) · [`response-envelope.json`](../schemas/response-envelope.json) — `error.code` carries an `ExitCode` value; the full error object is defined in `ResponseEnvelope.ErrorDetail`
