# REQ-F-015: Validate-Before-Execute Phase Order

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§14 Argument Validation Before Side Effects](../challenges/02-critical-execution-and-reliability/14-high-arg-validation.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST enforce a strict two-phase execution model for every command: all registered `validate()` hooks MUST complete successfully before any registered `execute()` hook is called. The framework MUST make it structurally impossible for a command to initiate a side effect inside a validation hook. Validation errors MUST be collected in full (all errors, not just the first) before reporting.

## Acceptance Criteria

- A command with two validation errors reports both in a single invocation (not one per run).
- A command that fails validation never writes to the filesystem, network, or any external state.
- The framework raises a registration error if a command registers an `execute()` hook that is called before all `validate()` hooks complete.
- Validation failures always exit with code `2`.
