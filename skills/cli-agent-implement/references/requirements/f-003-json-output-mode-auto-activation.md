# REQ-F-003: JSON Output Mode Auto-Activation

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§2 Output Format & Parseability](../challenges/04-critical-output-and-parsing/02-critical-output-format.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Medium / Context: High

---

## Description

The framework MUST automatically activate structured JSON output when stdout is not a TTY, or when the `CI` environment variable is set to any non-empty value, or when `NO_COLOR` is set. Command authors MUST NOT need to check for these conditions themselves; the framework handles format selection. When JSON mode is active, stdout MUST contain only valid JSON; all prose MUST be routed to stderr.

## Acceptance Criteria

- When `isatty(stdout) == false`, output is valid JSON without any additional configuration.
- When `CI=true`, output is valid JSON regardless of TTY state.
- A command author who calls only the framework's `output()` function never produces invalid JSON in non-TTY contexts.
- `python -c "import json,sys; json.load(sys.stdin)"` succeeds on every line of stdout in non-TTY mode.
