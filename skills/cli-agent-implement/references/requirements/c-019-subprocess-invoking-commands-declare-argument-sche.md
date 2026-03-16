# REQ-C-019: Subprocess-Invoking Commands Declare Argument Schema

**Tier:** Command Contract | **Priority:** P1

**Source:** [§34 Shell Injection via Agent-Constructed Commands](../challenges/01-critical-ecosystem-runtime-agent-specific/34-critical-shell-injection.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

Any command that invokes a subprocess with arguments derived from user input MUST declare in its registration schema: the subprocess binary name, which of its arguments originate from user input (by field name), and which arguments are framework-hardcoded. The framework enforces this declaration at registration and uses it to apply REQ-F-044 metacharacter rejection to exactly the user-derived arguments. Commands MUST use the framework's `subprocess()` API rather than raw `os.system()`, `subprocess.Popen(shell=True)`, or `child_process.exec()`.

## Acceptance Criteria

- A command using the framework's `subprocess()` API with a user-supplied argument is automatically protected by REQ-F-044.
- A command that uses `os.system()` directly is flagged by the framework's registration linter.
- The `--schema` output for subprocess-invoking commands includes a `subprocess` section listing the binary and user-controlled arguments.
- An attempt to pass a shell metacharacter in a user-derived subprocess argument is rejected with exit code 2.
