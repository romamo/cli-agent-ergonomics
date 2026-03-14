# REQ-F-050: Update Notifier Side-Channel Suppression

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§41 Update Notifier Side-Channel Output Pollution](../challenges/01-critical-ecosystem-runtime-agent-specific/41-high-update-notifier.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: High

---

## Description

In non-TTY mode and when `CI` is set, the framework MUST suppress all update/upgrade notification output on both stdout and stderr. The suppression MUST be applied by: setting `CI=1` (suppresses most Node.js package update notifiers), `NO_UPDATE_NOTIFIER=1`, `HOMEBREW_NO_AUTO_UPDATE=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and any other environment variables appropriate to the host runtime. The framework MUST provide a registration hook `suppress_update_notifier(fn)` for command authors to register custom suppression logic for third-party libraries that check updates in non-standard ways.

## Acceptance Criteria

- A command that uses a library with a built-in update notifier produces no update notification on stdout or stderr in non-TTY mode.
- The suppression environment variables are set before any command execution.
- `CI=1` is set in the subprocess environment for all child processes spawned by the framework.
- In TTY mode, update notifications are unaffected (shown as normal).
