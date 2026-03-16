# REQ-C-015: Commands Declare Input and Output Schema

**Tier:** Command Contract | **Priority:** P1

**Source:** [§21 Schema & Help Discoverability](../challenges/06-high-errors-and-discoverability/21-medium-schema-discoverability.md)

**Addresses:** Severity: Medium / Token Spend: High / Time: Medium / Context: Medium

---

## Description

Every command MUST declare a complete input schema (all parameters: name, type, required, default, enum values if applicable, description) and output schema (JSON Schema for the `data` field of the response envelope). The framework MUST auto-generate `--schema` output from these declarations. Command authors MUST NOT write `--schema` output manually; it MUST be derived from the declaration.

## Acceptance Criteria

- `tool <cmd> --schema` returns valid JSON containing `parameters` and `output_schema`.
- `tool --schema` returns a manifest of all commands with their parameter and output schemas.
- Adding a parameter to a command automatically appears in `--schema` without separate documentation effort.
- The `output_schema` is a valid JSON Schema object.
