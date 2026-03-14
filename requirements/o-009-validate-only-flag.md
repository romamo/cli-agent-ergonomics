# REQ-O-009: --validate-only Flag

**Tier:** Opt-In | **Priority:** P1

**Source:** [§14 Argument Validation Before Side Effects](../challenges/02-critical-execution-and-reliability/14-high-arg-validation.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST provide `--validate-only` as a standard flag on every command. When passed, the framework runs Phase 1 (validation) and reports results, then exits without running Phase 2 (execution). Exit `0` means all validation passed and the command would succeed. Exit `2` means validation errors were found, listed in the JSON error response. This flag MUST be registered automatically by the framework; command authors do not implement it.

## Acceptance Criteria

- `--validate-only` with valid args exits `0` with a JSON response indicating validation passed.
- `--validate-only` with invalid args exits `2` with all validation errors listed.
- `--validate-only` never causes any side effects, even when called with perfectly valid args.
- The `--validate-only` flag is present in every command's `--help` output.
