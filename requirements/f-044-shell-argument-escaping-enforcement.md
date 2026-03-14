# REQ-F-044: Shell Argument Escaping Enforcement

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§34 Shell Injection via Agent-Constructed Commands](../challenges/01-critical-ecosystem-runtime-agent-specific/34-critical-shell-injection.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST provide subprocess invocation APIs that never construct shell command strings. All subprocess calls MUST use exec-array style (argument list, not shell string) APIs, bypassing the shell entirely. The framework MUST prohibit `shell=True` (Python), `sh -c <string>` composition, and equivalent patterns. When the framework detects that a command argument contains shell metacharacters (`; | & $ ( ) < > \` \n \r`), it MUST reject the argument with exit code 2 before execution. This protection applies to all arguments derived from user input, environment variables, and prior command output.

## Acceptance Criteria

- A subprocess invocation via the framework API with a user-supplied argument containing `; rm -rf /` succeeds or rejects the argument cleanly — it MUST NOT execute the injected command.
- The framework's subprocess API raises a registration error if `shell=True` is passed.
- An argument containing a newline character is rejected in Phase 1 with exit code 2.
- Shell metacharacter rejection is documented in the framework's command author guide.
