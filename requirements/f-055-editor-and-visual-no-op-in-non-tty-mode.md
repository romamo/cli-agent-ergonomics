# REQ-F-055: $EDITOR and $VISUAL No-Op in Non-TTY Mode

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§62 $EDITOR and $VISUAL Trap](../challenges/01-critical-ecosystem-runtime-agent-specific/62-critical-editor-trap.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST set `EDITOR=true` and `VISUAL=true` (or equivalent no-op commands) in the environment of all spawned subprocesses when stdin/stdout are not a TTY. This prevents any subprocess from launching an interactive text editor. Additionally, if the framework detects that a command has invoked `$EDITOR` or `$VISUAL` in non-TTY mode (via the subprocess API), it MUST intercept the invocation, exit with code 4, and emit a structured error listing the non-interactive alternative flag (e.g., `--message`, `--from-file`).

## Acceptance Criteria

- In non-TTY mode, `git commit` invoked via the framework's subprocess API does not open vim.
- A command that calls `os.environ['EDITOR']` to launch an editor exits with code 4 in non-TTY mode.
- The exit 4 error includes `alternatives[]` listing non-interactive flags for the same operation.
- In TTY mode, `$EDITOR` is unmodified and interactive editing works normally.
