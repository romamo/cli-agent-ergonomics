# REQ-F-002: Exit Code 2 Reserved for Validation Failures

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§1 Exit Codes & Status Signaling](../challenges/04-critical-output-and-parsing/01-critical-exit-codes.md) · [§14 Argument Validation Before Side Effects](../challenges/02-critical-execution-and-reliability/14-high-arg-validation.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Low

---

## Description

The framework MUST ensure that exit code `2` is emitted if and only if command execution was aborted during input validation, before any side effect occurred. The framework MUST guarantee this by enforcing the validate-before-execute phase boundary (see REQ-F-015). A command that exits `2` MUST be safe to retry without any cleanup or rollback.

## Acceptance Criteria

- A command that exits `2` has provably caused zero filesystem, network, or state mutations.
- No command in the framework exits `2` after any side effect has been initiated.
- The JSON error response for exit `2` MUST include `"phase": "validation"`.
