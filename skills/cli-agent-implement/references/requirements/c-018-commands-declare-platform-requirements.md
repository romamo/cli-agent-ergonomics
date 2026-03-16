# REQ-C-018: Commands Declare Platform Requirements

**Tier:** Command Contract | **Priority:** P3

**Source:** [§27 Platform & Shell Portability](../challenges/05-high-environment-and-state/27-medium-platform-portability.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

Commands that have platform-specific requirements MUST declare them in their registration metadata: `platform` (array of supported OS names), `shell_requirements` (minimum shell version if applicable), and `required_tools` (array of external tool dependencies with minimum versions). The framework uses this information to populate `tool doctor` checks (REQ-O-026) and to emit a warning when a command is invoked on an unsupported platform.

## Acceptance Criteria

- `tool doctor` reports a check failure for each missing or outdated required tool.
- Invoking a Linux-only command on macOS emits a compatibility warning in `meta.warnings`.
- The `--schema` output for each command includes `platform` and `required_tools`.
