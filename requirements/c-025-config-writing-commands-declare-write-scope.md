# REQ-C-025: Config-Writing Commands Declare Write Scope

**Tier:** Command Contract | **Priority:** P0

**Source:** [§65 Global Configuration State Contamination](../challenges/01-critical-ecosystem-runtime-agent-specific/65-high-global-config-contamination.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

Any command that writes to a configuration file MUST declare `config_write_scope: "local" | "global" | "session"` in its registration metadata. Commands with `config_write_scope: "global"` MUST require an explicit `--global` flag from the caller and MUST emit a `GLOBAL_CONFIG_MODIFIED` warning in the JSON response. The framework defaults all config writes to `local` scope (nearest `.tool-config` in the directory hierarchy). Global config writes MUST use atomic rename to prevent partial-write corruption and MUST acquire an advisory lock before writing.

## Acceptance Criteria

- A config-write command without `--global` writes to `./.tool-config`, not `~/.config/tool/`.
- `--global` causes a write to `~/.config/tool/` AND emits `GLOBAL_CONFIG_MODIFIED` in `warnings[]`.
- Omitting `config_write_scope` from a config-writing command raises a framework registration warning.
- A global config write interrupted mid-way leaves the previous config intact (atomic rename).
