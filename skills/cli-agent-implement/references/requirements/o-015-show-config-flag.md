# REQ-O-015: --show-config Flag

**Tier:** Opt-In | **Priority:** P1

**Source:** [§28 Config File Shadowing & Precedence](../challenges/05-high-environment-and-state/28-high-config-shadowing.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST provide `tool --show-config` as a built-in invocation that outputs the effective resolved configuration, with per-key source attribution. The output MUST be JSON and MUST include: `effective_config` (resolved key-value map), `sources` (per-key source: which file or env var provided the value), and `precedence_order` (the canonical list of config sources in precedence order). This MUST reflect the state for the given invocation context (CWD, env vars at invocation time).

## Acceptance Criteria

- `tool --show-config --output json | python -c "import json,sys; json.load(sys.stdin)"` succeeds.
- Each key in `sources` maps to the file path or env var name that provided its value.
- `precedence_order` is present and lists all config layers in order.
- The output reflects the actual resolved state, including any env var overrides.
