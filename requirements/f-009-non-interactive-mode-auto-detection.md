# REQ-F-009: Non-Interactive Mode Auto-Detection

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§10 Interactivity & TTY Requirements](../challenges/02-critical-execution-and-reliability/10-critical-interactivity.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST automatically detect non-interactive execution by checking whether stdin is a TTY (`isatty(stdin)`). When stdin is not a TTY, the framework MUST globally disable all interactive prompts and treat the session as `--non-interactive`. Commands MUST NOT block waiting for stdin input in non-interactive mode; instead, they MUST fail immediately with a structured error (exit code 4) if required input is unavailable.

## Acceptance Criteria

- A command that would prompt for input in TTY mode exits immediately with exit code 4 and a JSON error when stdin is `/dev/null`.
- No command hangs waiting for stdin input when `isatty(stdin) == false`.
- The JSON error for this condition includes `"code": "INPUT_REQUIRED"` and a `suggestion` field.
