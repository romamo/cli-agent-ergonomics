# REQ-F-010: Pager Suppression

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§10 Interactivity & TTY Requirements](../challenges/02-critical-execution-and-reliability/10-critical-interactivity.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST set `PAGER=cat` and `GIT_PAGER=cat` in the process environment before executing any command. The framework MUST NOT invoke any pager program for its own output. Any child process spawned by the framework inherits these environment variable overrides.

## Acceptance Criteria

- Running any command with a large output does not block on pager input.
- `echo $PAGER` in a child shell spawned by a framework command returns `cat`.
- `git log` executed as a sub-command from within a framework command does not open a pager.
