# REQ-F-027: CWD in Response Meta

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§29 Working Directory Sensitivity](../challenges/05-high-environment-and-state/29-medium-working-directory.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: Low

---

## Description

The framework MUST automatically inject `meta.cwd` (the process working directory at the time of invocation) into every response. For commands that discover a project root (walking up the directory tree), the framework MUST also inject `meta.project_root` when the command declares a root-resolution behavior.

## Acceptance Criteria

- Every response includes `meta.cwd` as an absolute path string.
- `meta.cwd` matches the result of `pwd` in the shell that invoked the command.
- Commands that resolve a project root include `meta.project_root` as an absolute path.
