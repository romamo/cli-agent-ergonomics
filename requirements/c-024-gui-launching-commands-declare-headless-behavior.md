# REQ-C-024: GUI-Launching Commands Declare Headless Behavior

**Tier:** Command Contract | **Priority:** P1

**Source:** [§64 Headless Display and GUI Launch Blocking](../challenges/01-critical-ecosystem-runtime-agent-specific/64-critical-headless-gui.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

Any command that launches a GUI application, opens a browser, or invokes a display-requiring subprocess MUST declare `gui_operations: [<list of operation types>]` and `headless_behavior: <"emit_in_output" | "skip" | "error">` in its registration metadata. The framework raises a registration error if `gui_operations` is non-empty without `headless_behavior`. In headless mode, the framework enforces the declared behavior automatically: `emit_in_output` places the URL/path in the JSON response, `skip` omits the operation with a warning, `error` exits 4.

## Acceptance Criteria

- A command with `gui_operations: ["browser_open"]` and `headless_behavior: "emit_in_output"` returns `data.open_url` in headless mode.
- A command with `gui_operations: ["browser_open"]` but no `headless_behavior` raises a registration error.
- In non-headless mode, the GUI operation proceeds normally.
- `meta.headless: true` is included in all responses when headless mode is active.
