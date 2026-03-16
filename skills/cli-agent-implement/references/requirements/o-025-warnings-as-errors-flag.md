# REQ-O-025: --warnings-as-errors Flag

**Tier:** Opt-In | **Priority:** P3

**Source:** [§3 Stderr vs Stdout Discipline](../challenges/04-critical-output-and-parsing/03-high-stderr-stdout.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: High

---

## Description

The framework MUST provide `--warnings-as-errors` as a standard flag. When passed, any warning emitted via the framework's `warn()` API causes the command to exit non-zero (exit code `1`) after completing, and the `warnings` array in the JSON response MUST be non-empty. This is useful for strict automated pipelines that must not silently continue past deprecated usage or unexpected conditions.

## Acceptance Criteria

- A command that emits no warnings exits `0` even with `--warnings-as-errors`.
- A command that emits one warning exits `1` when `--warnings-as-errors` is passed.
- The `warnings` array in the response contains the warning that triggered the exit.
- Without `--warnings-as-errors`, warnings are emitted but do not affect exit code.
