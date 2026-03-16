# REQ-F-023: Tool Version in Every Response

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§22 Schema Versioning & Output Stability](../challenges/06-high-errors-and-discoverability/22-high-schema-versioning.md) · [§32 Self-Update & Auto-Upgrade Behavior](../challenges/05-high-environment-and-state/32-high-self-update.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST automatically inject `meta.tool_version` (semver string of the running tool binary) and, when an update is available, `meta.update_available` (semver string of the latest version) into every response. The update availability check MUST be non-blocking and MUST NOT delay command execution. If the update check fails, `meta.update_available` MUST be omitted (not set to an error value).

## Acceptance Criteria

- Every response includes `meta.tool_version`.
- `meta.tool_version` matches the output of `tool --version`.
- `meta.update_available` is absent (not null, absent) when no update is available or check failed.
- The update check does not add measurable latency to command execution.
