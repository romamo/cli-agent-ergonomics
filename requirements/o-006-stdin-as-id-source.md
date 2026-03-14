# REQ-O-006: Stdin as ID Source (-)

**Tier:** Opt-In | **Priority:** P3

**Source:** [§6 Command Composition & Piping](../challenges/04-critical-output-and-parsing/06-medium-command-composition.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: Low

---

## Description

The framework MUST support the convention that any argument accepting an identifier value also accepts `-` to mean "read the value from stdin". Command authors declare arguments as `pipe_compatible: true`; the framework handles stdin reading transparently. This enables shell composition: `tool get-user --name Alice --output id | tool delete-user --id -`.

## Acceptance Criteria

- `echo 42 | tool delete-user --id -` is equivalent to `tool delete-user --id 42`.
- Reading from `-` works when stdin is a pipe and when stdin is a file redirect.
- An error is raised if `-` is passed but stdin has no data (empty stdin).
