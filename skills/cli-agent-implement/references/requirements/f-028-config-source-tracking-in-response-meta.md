# REQ-F-028: Config Source Tracking in Response Meta

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§28 Config File Shadowing & Precedence](../challenges/05-high-environment-and-state/28-high-config-shadowing.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST automatically inject `meta.config_sources` (array of config file paths that were loaded, in precedence order) and `meta.effective_config_hash` (a short stable hash of the resolved configuration) into every response. This allows callers to detect when configuration has changed between invocations without needing to call `--show-config` separately.

## Acceptance Criteria

- Every response includes `meta.config_sources` as an array of absolute path strings.
- `meta.effective_config_hash` changes when any config file is modified.
- `meta.effective_config_hash` is stable when no config has changed.
- The array is empty (not absent) when no config files were loaded.
