# REQ-O-016: --no-config Flag

**Tier:** Opt-In | **Priority:** P1

**Source:** [§28 Config File Shadowing & Precedence](../challenges/05-high-environment-and-state/28-high-config-shadowing.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST provide `--no-config` as a standard flag on every command. When passed, the framework MUST skip loading all config files (local `.toolrc`, user `~/.config/tool/config.*`, and system `/etc/tool/config.*`). Environment variable overrides MUST still apply (they are not "config files"). With `--no-config`, behavior MUST depend only on explicit CLI flags and compiled-in defaults, making the invocation fully reproducible regardless of the execution environment's config files.

## Acceptance Criteria

- `--no-config` causes no config file to be read, regardless of what files exist.
- Environment variables still take effect with `--no-config`.
- `meta.config_sources` is an empty array when `--no-config` is passed.
- `--no-config` is present in every command's `--help` output.
