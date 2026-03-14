# REQ-F-007: ANSI/Color Code Suppression

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§8 ANSI & Color Code Leakage](../challenges/04-critical-output-and-parsing/08-high-ansi-leakage.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: Medium

---

## Description

The framework MUST strip all ANSI escape sequences from every string value before JSON serialization, unconditionally in JSON output mode. The strip operation MUST cover: SGR color/style codes (`\x1b[...m`), cursor movement sequences, OSC sequences, and carriage return characters. This stripping MUST apply to all string fields including error messages and values derived from third-party libraries.

## Acceptance Criteria

- No byte in the range `\x1b` appears in the JSON output when in JSON mode.
- A string value that was injected with color codes by a third-party dependency is clean in the JSON output.
- JSON output passes `jq '.'` without error even when the process was invoked with a TTY.
