# REQ-C-020: Resource ID Fields Declare Validation Pattern

**Tier:** Command Contract | **Priority:** P1

**Source:** [§35 Agent Hallucination Input Patterns](../challenges/01-critical-ecosystem-runtime-agent-specific/35-high-hallucination-inputs.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

Any command argument declared as a resource identifier (e.g., ID, slug, name, key) MUST include an explicit validation pattern in its schema: either a regex, an enum of allowed values, or a reference to a built-in pattern type (`alphanumeric_id`, `uuid`, `semver`, `filepath`, `url`). Arguments using a built-in pattern type automatically receive the hallucination pattern checks from REQ-F-045. Arguments using a custom regex MUST use anchored patterns (`^...$`). The framework MUST apply the declared pattern in Phase 1 validation before any execution.

## Acceptance Criteria

- A command argument declared as type `alphanumeric_id` automatically rejects inputs containing `/`, `.`, `?`, `#`, and `%`.
- A command argument with a custom regex `^[a-z0-9-]{3,64}$` rejects inputs that do not match.
- A command argument with no declared pattern for a resource ID field triggers a framework registration warning.
- Pattern validation failures exit with code 2 and include the argument name and the expected pattern in the error.
