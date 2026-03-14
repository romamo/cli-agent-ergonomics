# REQ-O-005: --output id Extraction Mode

**Tier:** Opt-In | **Priority:** P3

**Source:** [§6 Command Composition & Piping](../challenges/04-critical-output-and-parsing/06-medium-command-composition.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: Low

---

## Description

The framework MUST support `--output id` as a format option on any command that returns a primary identifier. In this mode, stdout MUST contain only the bare identifier string (no JSON, no newline except the terminal one). Commands declare their primary identifier field; the framework extracts and emits it. This mode is designed for shell piping: `tool get-user --name Alice --output id | tool send-email --user-id -`.

## Acceptance Criteria

- `--output id` on a command that returns `{"data": {"id": 42}}` produces `42\n` on stdout.
- The output is directly pipeable to another command's stdin.
- No JSON structure, no whitespace beyond the terminal newline, is present in the output.
