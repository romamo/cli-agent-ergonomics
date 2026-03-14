# REQ-F-062: Glob Expansion and Word-Splitting Prevention

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§51 Shell Word Splitting and Glob Expansion Interference](../challenges/01-critical-ecosystem-runtime-agent-specific/51-high-glob-expansion.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework's subprocess API MUST always invoke external processes using array-form argument lists, never via shell string interpolation. The framework MUST raise a registration error if a command handler passes a shell-string (single joined string) to the subprocess API instead of an argument array. This prevents the shell from performing word-splitting on arguments containing spaces and glob expansion on arguments containing `*`, `?`, or `[`. When the framework logs subprocess invocations (in debug mode), it MUST display the array form to make quoting visible.

## Acceptance Criteria

- An argument containing spaces (e.g., `"hello world"`) is received by the subprocess as a single argument, not split into two.
- An argument containing `*` (e.g., `"*.json"`) is passed literally to the subprocess, not expanded by the shell.
- Passing a shell-string to the subprocess API raises a framework `SHELL_STRING_PROHIBITED` error at registration time.
- In debug mode, subprocess invocations are logged as JSON arrays: `["git", "commit", "-m", "hello world"]`.
