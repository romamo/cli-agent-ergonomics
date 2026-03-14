# REQ-F-041: Process CWD Immutability

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§29 Working Directory Sensitivity](../challenges/05-high-environment-and-state/29-medium-working-directory.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: Low

---

## Description

The framework MUST prohibit commands from changing the process working directory (`os.chdir()` or equivalent) during execution. If a command's implementation requires operating in a different directory, it MUST do so by constructing absolute paths, not by changing the process CWD. The framework SHOULD detect and warn at registration time if a command registers a hook that calls `chdir`.

## Acceptance Criteria

- The process CWD after any command invocation is identical to the CWD before invocation.
- A command that internally calls `os.chdir()` is flagged by the framework's linter/registration check.
- Operations on files in other directories work correctly using absolute paths constructed from `--cwd` (REQ-O-017).
