# REQ-O-024: --context / --config Override Flag

**Tier:** Opt-In | **Priority:** P1

**Source:** [§26 Stateful Commands & Session Management](../challenges/05-high-environment-and-state/26-high-session-management.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST provide `--context <name>` (select a named context from the config file) and `--config <path>` (use a specific config file instead of the default) as standard flags on every command. These flags MUST allow complete isolation between agent sessions that share a filesystem: each session passes `--config /tmp/agent-session-N/config.json` to prevent state conflicts. When `--context` is passed, it MUST override any context set by prior `use-context` style commands.

## Acceptance Criteria

- `--config /tmp/isolated.json` causes the command to load config only from that file.
- `--context staging` causes the command to use the `staging` context from the loaded config.
- Two concurrent invocations with different `--config` paths do not share any mutable state.
- `meta.config_sources` reflects the `--config` path when passed.
