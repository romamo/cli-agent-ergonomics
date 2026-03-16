# REQ-C-014: Error Responses Include retryable and retry_after_ms

**Tier:** Command Contract | **Priority:** P1

**Source:** [§19 Retry Hints in Error Responses](../challenges/06-high-errors-and-discoverability/19-high-retry-hints.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

Every error response MUST include `error.retryable` (boolean or the string `"maybe"`) indicating whether the same invocation with identical arguments is safe to retry. For retryable errors, the response SHOULD include `error.retry_after_ms` (integer milliseconds to wait before retrying) and `error.retry_strategy` (one of: `"immediate"`, `"linear_backoff"`, `"exponential_backoff"`). The framework MUST maintain a default `retryable` value for each error code in its error registry, which commands inherit unless overridden.

## Acceptance Criteria

- Every error response includes `error.retryable`.
- A `RATE_LIMITED` error includes `error.retry_after_ms > 0`.
- A `VALIDATION_ERROR` error has `error.retryable: false`.
- A `TIMEOUT` error has `error.retryable: true`.
- The framework error registry maps all standard error codes to default `retryable` values.
