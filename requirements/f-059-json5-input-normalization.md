# REQ-F-059: JSON5 Input Normalization

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§67 Agent-Generated Input Syntax Rejection](../challenges/01-critical-ecosystem-runtime-agent-specific/67-high-json5-input.md)

**Addresses:** Severity: High / Token Spend: High / Time: Medium / Context: Low

---

## Description

The framework MUST use a forgiving JSON parser for all structured input flags (`--config`, `--filter`, `--data`, `--raw-payload`, and any flag declared with `type: json`). The parser MUST accept: trailing commas in objects and arrays, single-line `//` comments, block `/* */` comments, and unquoted keys. When strict JSON parsing is required (e.g., for schema validation), the framework MUST normalize the input to strict JSON first. If normalization fails, the error MUST include a `corrected_input` field showing the normalized form that would have been accepted.

## Acceptance Criteria

- `--config '{"key": "value",}'` (trailing comma) is accepted and parsed correctly.
- `--config '{"key": "value" /* comment */}'` is accepted and parsed correctly.
- A malformed input that cannot be normalized produces an error with `corrected_input` showing the closest valid form.
- Normalized inputs pass JSON schema validation identically to equivalent strict JSON.
