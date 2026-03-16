# REQ-O-013: --schema / --output-schema Flag

**Tier:** Opt-In | **Priority:** P1

**Source:** [§21 Schema & Help Discoverability](../challenges/06-high-errors-and-discoverability/21-medium-schema-discoverability.md)

**Addresses:** Severity: Medium / Token Spend: High / Time: Medium / Context: Medium

---

## Description

The framework MUST provide `tool --schema` (full manifest of all commands) and `tool <cmd> --output-schema` (JSON Schema for the `data` field of a specific command's response). Both MUST produce valid, machine-parseable JSON. The schemas MUST be generated automatically from command registration metadata (REQ-C-015). The full manifest MUST include: command name, description, danger level, parameters, output schema, exit codes, and stability tier per field.

## Acceptance Criteria

- `tool --schema | python -c "import json,sys; json.load(sys.stdin)"` succeeds.
- The schema includes `parameters`, `output_schema`, `exit_codes`, and `danger_level` for each command.
- `tool <cmd> --output-schema` is a valid JSON Schema that the command's `data` field conforms to.
- The schema output is stable (does not change between invocations absent registration changes).
