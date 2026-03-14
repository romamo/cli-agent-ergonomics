# REQ-C-010: Background-Process Commands Declare Metadata

**Tier:** Command Contract | **Priority:** P2

**Source:** [§17 Child Process Leakage](../challenges/02-critical-execution-and-reliability/17-medium-child-process-leakage.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Low

---

## Description

Any command that intentionally spawns a long-running background process MUST declare `spawns_background_process: true` in its registration metadata, and MUST declare `cleanup_command` (the framework command to stop the background process) and `max_lifetime_seconds` (after which the framework may kill it). The command MUST include `background_pid` and `cleanup_command` in its response `data`.

## Acceptance Criteria

- The `--schema` output for commands that spawn background processes includes `spawns_background_process: true`.
- The response `data` includes `background_pid` (integer) and `cleanup_command` (string).
- The framework refuses to register a command that spawns a background process without declaring this metadata.
