# REQ-O-038: --heartbeat-ms Flag for Long-Running Commands

**Tier:** Opt-In | **Priority:** P1

**Source:** [§60 OS Output Buffer Deadlock](../challenges/01-critical-ecosystem-runtime-agent-specific/60-critical-output-buffer-deadlock.md) · [§49 Async Job / Polling Protocol Absence](../challenges/01-critical-ecosystem-runtime-agent-specific/49-high-async-job-polling.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST provide `--heartbeat-ms <milliseconds>` (default: `10000`) for commands that may run longer than their timeout. When active, the framework emits a JSON heartbeat object to stdout at the specified interval: `{"status": "running", "heartbeat": true, "elapsed_ms": N, "step": "<current step if known>"}`. Heartbeats MUST be valid JSON lines compatible with JSONL streaming. The heartbeat interval MUST be configurable; `--heartbeat-ms 0` disables heartbeats.

## Acceptance Criteria

- A 25-second command with `--heartbeat-ms 10000` emits at least 2 heartbeat objects before the final result.
- Each heartbeat is a valid JSON object parseable independently.
- The final response (success or failure) is also a valid JSON object and is distinguishable from heartbeats by `"heartbeat": false` or absence of the `heartbeat` field.
- `--heartbeat-ms 0` produces no heartbeat objects.
