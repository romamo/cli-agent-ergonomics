# REQ-C-006: All Args Validated in Phase 1

**Tier:** Command Contract | **Priority:** P0

**Source:** [§14 Argument Validation Before Side Effects](../challenges/02-critical-execution-and-reliability/14-high-arg-validation.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

Command authors MUST implement all argument and precondition validation within the command's `validate()` hook, not within `execute()`. The `validate()` hook MUST be free of side effects. Validation MUST check all arguments at once, collecting all errors before returning (not fail-fast on the first error). The framework enforces phase ordering (REQ-F-015) but depends on command authors correctly placing validation logic.

## Acceptance Criteria

- A command with multiple invalid arguments reports all validation errors in a single invocation.
- A validation hook that attempts to write a file is caught by the framework's side-effect detector (if implemented) or flagged in code review by the framework's linting rules.
- The validation phase completes in under 100ms for all commands (no network calls in validate()).
- Validation errors reference the specific parameter name and value that failed.
