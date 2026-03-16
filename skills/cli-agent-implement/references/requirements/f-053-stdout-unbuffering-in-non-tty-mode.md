# REQ-F-053: Stdout Unbuffering in Non-TTY Mode

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§60 OS Output Buffer Deadlock](../challenges/01-critical-ecosystem-runtime-agent-specific/60-critical-output-buffer-deadlock.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST disable OS-level stdout buffering when stdout is not a TTY. In Python this means calling `sys.stdout.reconfigure(line_buffering=True)` and setting `PYTHONUNBUFFERED=1` before any output. In Node.js this means calling `process.stdout.cork()` / `uncork()` appropriately or using unbuffered streams. This MUST be performed in the framework's bootstrap, before any command code runs. For long-running commands (>5s), the framework MUST additionally emit a JSON heartbeat object to stdout every configurable interval (default: 10000ms) via the `--heartbeat-ms` flag (REQ-O-038).

## Acceptance Criteria

- A command that emits one log line per second is received by the agent one line at a time, not in a single flush after the process exits.
- `PYTHONUNBUFFERED=1` is set in the process environment before the first `output()` call.
- A 30-second command with heartbeats enabled emits at least 2 heartbeat JSON objects to stdout before completing.
- Heartbeat objects are valid JSON matching `{"status": "running", "heartbeat": true, "elapsed_ms": N}`.
