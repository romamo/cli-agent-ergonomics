# REQ-F-038: Verbosity Auto-Quiet in Non-TTY Context

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§4 Verbosity & Token Cost](../challenges/04-critical-output-and-parsing/04-medium-verbosity.md)

**Addresses:** Severity: Medium / Token Spend: High / Time: Low / Context: High

---

## Description

When stdout is not a TTY or when `CI` is set, the framework MUST automatically suppress all non-essential prose from stderr (equivalent to `--quiet`). Only the structured JSON output on stdout and explicit errors on stderr MUST remain. Command authors MUST NOT need to check TTY state themselves; the framework's `log()` and `progress()` primitives respect this mode automatically.

## Acceptance Criteria

- In a non-TTY context, `progress()` calls produce no output.
- In a non-TTY context, `log()` calls at level INFO and below produce no stderr output.
- Error-level `log()` calls are always emitted regardless of TTY state.
- Explicitly passing `--verbose` overrides auto-quiet mode.
