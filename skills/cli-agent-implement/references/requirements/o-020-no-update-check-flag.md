# REQ-O-020: --no-update-check Flag

**Tier:** Opt-In | **Priority:** P1

**Source:** [§32 Self-Update & Auto-Upgrade Behavior](../challenges/05-high-environment-and-state/32-high-self-update.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

The framework MUST provide `--no-update-check` as a standard flag on every command. When passed (or when `TOOL_NO_UPDATE` is set), the framework MUST skip any update availability check for that invocation. This flag MUST be respected even in interactive TTY contexts where update checks are otherwise enabled. The flag MUST be visible in `--help` output.

## Acceptance Criteria

- `--no-update-check` prevents any network call for update checking.
- `--no-update-check` and `TOOL_NO_UPDATE=1` are equivalent in effect.
- `meta.update_available` is absent when `--no-update-check` is passed.
- The flag is present in every command's `--help` output.
