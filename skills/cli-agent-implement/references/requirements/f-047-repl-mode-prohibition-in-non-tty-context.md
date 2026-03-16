# REQ-F-047: REPL Mode Prohibition in Non-TTY Context

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§37 REPL / Interactive Mode Accidental Triggering](../challenges/01-critical-ecosystem-runtime-agent-specific/37-critical-repl-triggering.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

When stdin is not a TTY, the framework MUST detect and prevent entry into any interactive REPL, shell, or prompt loop. The framework MUST intercept: commands invoked with no subcommand (if the default behavior would enter an interactive shell), `input()` / `readline()` calls that would block on stdin, and any prompt library invocation. If a would-be-blocking interactive call is detected at runtime in non-TTY mode, the framework MUST immediately exit with code 4 and a structured error: `{"ok": false, "error": {"code": "INTERACTIVE_BLOCKED", "message": "Command requires interactive input but stdin is not a TTY."}}`.

## Acceptance Criteria

- A command that calls `input()` in non-TTY mode exits with code 4 and structured JSON error, not a hang.
- A CLI invoked with no arguments that would drop into REPL mode exits with code 4 in non-TTY mode.
- In TTY mode, interactive prompts are unaffected.
- The error message includes specific guidance on which flag to pass to run non-interactively.
