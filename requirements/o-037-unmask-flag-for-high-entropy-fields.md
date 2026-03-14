# REQ-O-037: --unmask Flag for High-Entropy Fields

**Tier:** Opt-In | **Priority:** P2

**Source:** [§59 High-Entropy String Token Poisoning](../challenges/01-critical-ecosystem-runtime-agent-specific/59-high-high-entropy-tokens.md)

**Addresses:** Severity: High / Token Spend: High / Time: Low / Context: High

---

## Description

The framework MUST provide `--unmask` as a global flag that disables the high-entropy masking from REQ-F-058. When `--unmask` is passed, all fields are returned with their raw values. This flag SHOULD require explicit invocation and MUST NOT be activated by any environment variable. The `--unmask` flag is intended for debugging and human inspection; agents should not pass it except when they specifically need the raw high-entropy value for a subsequent operation.

## Acceptance Criteria

- Without `--unmask`, a JWT field is returned as `[JWT: sub=..., exp=...]`.
- With `--unmask`, the same field returns the full raw JWT string.
- `--unmask` cannot be activated via environment variable.
- `--schema` documents `--unmask` and notes that it exposes sensitive values.
