# REQ-O-017: --cwd / --root Flag

**Tier:** Opt-In | **Priority:** P2

**Source:** [§29 Working Directory Sensitivity](../challenges/05-high-environment-and-state/29-medium-working-directory.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: Low

---

## Description

The framework MUST provide `--cwd <path>` as a standard flag on all commands that interact with the filesystem. When `--cwd` is passed, the framework resolves all relative paths against the given path instead of the process CWD. The framework MUST validate that the path exists and is a directory before execution (exit `2` if not). The effective CWD used MUST be recorded in `meta.cwd`.

## Acceptance Criteria

- `--cwd /project` causes all relative path resolution to be based on `/project`.
- `meta.cwd` reflects the value of `--cwd` when passed.
- A non-existent `--cwd` path causes exit `2` with a validation error before any side effects.
- `--cwd` does not change the process's actual working directory (REQ-F-041).
