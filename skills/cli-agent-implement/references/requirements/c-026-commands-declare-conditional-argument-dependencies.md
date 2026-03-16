# REQ-C-026: Commands Declare Conditional Argument Dependencies

**Tier:** Command Contract | **Priority:** P1

**Source:** [§54 Conditional / Dependent Argument Requirements](../challenges/01-critical-ecosystem-runtime-agent-specific/54-high-conditional-args.md)

**Addresses:** Severity: High / Token Spend: High / Time: Medium / Context: Low

---

## Description

Commands MUST declare all conditional argument requirements in their registration metadata using a `requires` clause, rather than discovering them at runtime. The `requires` clause specifies: when flag A has value V, flag B is required; when flag A is present, flag B is prohibited (mutual exclusion); when flag A is absent, flag B has a different default. The framework validates all declared `requires` relationships during the validate-before-execute phase (Phase 1), before any side effects. The `--schema` output MUST include the full `requires` graph so agents can construct valid calls without trial-and-error discovery.

## Acceptance Criteria

- A command with `requires: [{if: "--format=csv", then: "--separator"}]` exits 2 with a structured error when `--format csv` is passed without `--separator`.
- The `--schema` output includes the full conditional dependency graph.
- Mutually exclusive flags are enforced in Phase 1: passing both produces exit 2 before any I/O.
- An agent calling `--schema` can determine all required flags for a given combination of values without making a failing call first.
