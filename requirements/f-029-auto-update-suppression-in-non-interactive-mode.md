# REQ-F-029: Auto-Update Suppression in Non-Interactive Mode

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§32 Self-Update & Auto-Upgrade Behavior](../challenges/05-high-environment-and-state/32-high-self-update.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

The framework MUST disable any auto-update behavior (including update checks that add latency) when: `isatty(stdout) == false`, `CI` is set, `TOOL_NO_UPDATE` is set, or `--no-update-check` is passed. The framework MUST ensure that update availability information is surfaced only as a non-blocking `meta.update_available` field. The framework MUST ensure that the tool binary is never replaced while any instance is running.

## Acceptance Criteria

- No update check occurs when `CI=true`.
- No update check occurs when stdout is not a TTY.
- Setting `TOOL_NO_UPDATE=1` disables all update behavior including background checks.
- No measurable latency is added to any command due to update checking in non-interactive mode.
