# REQ-F-006: Stdout/Stderr Stream Enforcement

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§3 Stderr vs Stdout Discipline](../challenges/04-critical-output-and-parsing/03-high-stderr-stdout.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: High

---

## Description

The framework MUST provide separate output primitives: `output()` writes to stdout and `log()` / `progress()` / `warn()` write to stderr. The framework MUST route all internal framework messages (progress, debug, timing) to stderr. Command authors MUST NOT be able to accidentally write prose to stdout using the framework's API. Any unhandled exception caught by the framework MUST be serialized to stderr, not stdout.

## Acceptance Criteria

- When a command is run with `1>/dev/null`, no data output is lost.
- When a command is run with `2>/dev/null`, the structured result is still received on stdout.
- Stack traces from uncaught exceptions appear only on stderr, never on stdout.
- A command that calls only `log()` and `output()` produces valid JSON stdout with zero prose contamination.
