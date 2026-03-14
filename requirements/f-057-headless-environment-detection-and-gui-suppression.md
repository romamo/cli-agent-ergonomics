# REQ-F-057: Headless Environment Detection and GUI Suppression

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§64 Headless Display and GUI Launch Blocking](../challenges/01-critical-ecosystem-runtime-agent-specific/64-critical-headless-gui.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST detect headless execution environments on startup by checking: `sys.stdout.isatty()`, `CI` environment variable, `DISPLAY` and `WAYLAND_DISPLAY` environment variables (Linux/Unix), and `SSH_TTY`. When headless mode is detected, the framework MUST set `framework.headless = true` and intercept any attempt to launch a GUI application (browser open, file picker, notification dialog) via `xdg-open`, `webbrowser.open()`, `open` (macOS), or equivalent. Instead of launching, the framework MUST return the URL/path in the JSON response under `data.open_url` or `data.open_path` with a `meta.headless: true` indicator.

## Acceptance Criteria

- In a container without `$DISPLAY`, `xdg-open https://example.com` via framework API does not block; URL appears in `data.open_url`.
- `meta.headless: true` is set in all responses when headless mode is active.
- A command that declares `gui_operations: []` and attempts a GUI launch without headless behavior declared triggers a framework registration error.
- In TTY mode with `$DISPLAY` set, GUI launches proceed normally.
