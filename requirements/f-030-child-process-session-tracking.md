# REQ-F-030: Child Process Session Tracking

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§17 Child Process Leakage](../challenges/02-critical-execution-and-reliability/17-medium-child-process-leakage.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Low

---

## Description

When a command spawns any child process using the framework's process-spawning API, the framework MUST record the child PID in a session-scoped tracking file. On parent process exit (normal, error, or signal), the framework MUST attempt to terminate all tracked children. The tracking file path MUST be included in the command's response as `meta.session_pid_file` when any children were spawned.

## Acceptance Criteria

- After a command that spawns a child process exits, no orphaned child processes remain in the process table.
- The session tracking file exists and is readable while children are running.
- `SIGTERM` to the parent causes the framework to send `SIGTERM` to all tracked children before the parent exits.
