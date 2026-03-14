# REQ-O-032: --raw-payload Flag for Mutating Commands

**Tier:** Opt-In | **Priority:** P1

**Source:** [§46 API Schema to CLI Flag Translation Loss](../challenges/01-critical-ecosystem-runtime-agent-specific/46-high-api-translation-loss.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Medium

---

## Description

Mutating commands (those with `danger_level: "mutating"` or `"destructive"`) SHOULD support a `--raw-payload <json>` flag that accepts a raw JSON object mapped directly to the command's underlying API schema. When `--raw-payload` is used, the framework bypasses individual flag parsing and passes the payload directly to the command handler, enabling agents to pass API-native payloads with zero translation loss. The framework MUST validate `--raw-payload` content against the command's Pydantic or JSON Schema before execution. When `--raw-payload` and individual flags are both supplied, the framework MUST reject the invocation with exit code 2.

## Acceptance Criteria

- `command create --raw-payload '{"name": "foo", "count": 3}'` is equivalent to `command create --name foo --count 3`.
- Invalid `--raw-payload` JSON exits with code 2 and a structured field-level error.
- Supplying both `--raw-payload` and individual flags exits with code 2.
- The `--schema` output for mutating commands includes a `raw_payload_schema` section.
