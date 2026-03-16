# REQ-F-043: Temp File Session-Scoped Auto-Cleanup

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§30 Undeclared Filesystem Side Effects](../challenges/05-high-environment-and-state/30-medium-filesystem-side-effects.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Medium

---

## Description

The framework MUST automatically clean up the session-scoped temp directory (REQ-F-032) on normal command exit. For commands that produce output files intended for the caller to consume, the framework MUST include a `cleanup` object in the response containing `command` (the exact shell command to delete the file) and `auto_cleanup_after_seconds` (time after which the framework will delete the file if cleanup was not called). Background cleanup MUST NOT be implemented via a daemon; instead it MUST occur on next framework invocation.

## Acceptance Criteria

- After a command exits normally, its session temp directory no longer exists.
- A response that includes a caller-facing output file includes a `cleanup` object.
- `cleanup.command` is a valid, directly executable shell command.
- Files older than `auto_cleanup_after_seconds` are pruned when any framework command next runs.
