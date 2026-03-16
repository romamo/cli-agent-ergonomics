# REQ-C-023: Editor-Requiring Commands Declare Non-Interactive Alternative

**Tier:** Command Contract | **Priority:** P1

**Source:** [§62 $EDITOR and $VISUAL Trap](../challenges/01-critical-ecosystem-runtime-agent-specific/62-critical-editor-trap.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

Any command that invokes `$EDITOR` or `$VISUAL` MUST declare `requires_editor: true` in its registration metadata AND MUST declare at least one non-interactive alternative flag (e.g., `--message <text>`, `--from-file <path>`, `--content <text>`). The framework verifies this at registration and raises an error if `requires_editor: true` without a declared alternative. In non-TTY mode, the framework automatically uses the non-interactive alternative; if no value is provided for it, the command exits 4 with the alternative flag listed in the error.

## Acceptance Criteria

- A command with `requires_editor: true` but no declared alternative raises a registration error.
- In non-TTY mode, `git commit` equivalent exits 4 with `hint: "use --message <text> instead"`.
- Passing `--message "text"` in non-TTY mode bypasses the editor and proceeds normally.
- In TTY mode, the editor is invoked normally when neither alternative flag is provided.
