# REQ-F-060: Third-Party Stdout Interception

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§68 Third-Party Library Stdout Pollution](../challenges/01-critical-ecosystem-runtime-agent-specific/68-high-stdout-pollution.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: High

---

## Description

The framework MUST intercept all writes to file descriptor 1 (stdout) that are not made through the framework's `output()` API. Intercepted writes MUST be buffered, classified, and reclassified: prose writes (non-JSON) are moved to `warnings[]` with `code: "THIRD_PARTY_STDOUT"` and the raw text in `detail`; JSON-shaped writes are silently discarded (to prevent double-emission). The interception MUST be installed at the file descriptor level (not just the language runtime level) to capture writes from native extensions. The interception MUST be installed before any imports.

## Acceptance Criteria

- A library that calls `print("initialized")` on import does not contaminate the JSON stdout.
- The intercepted string appears as a warning: `{"code": "THIRD_PARTY_STDOUT", "detail": "initialized"}`.
- `json.loads(stdout_output)` succeeds even when a dependency prints to stdout.
- In debug mode (`--debug`), intercepted stdout is emitted to stderr with source attribution.
