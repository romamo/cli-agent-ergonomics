# REQ-F-077: Telemetry Non-Blocking

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** Silent assumption — agents calling a tool 500 times in a session cannot absorb synchronous telemetry latency; telemetry that fails must not affect exit code or output

**Addresses:** Severity: High / Token Spend: Low / Time: Medium / Context: Low

---

## Description

Any telemetry, analytics, error reporting, or update-check network call the framework makes MUST be:

1. **Async and fire-and-forget** — dispatched after stdout is flushed and the main process is ready to exit; never blocking the critical path
2. **Failure-transparent** — a failed telemetry call MUST NOT affect exit code, stdout output, or stderr output
3. **Opt-in or suppressed by `CI=true`** — telemetry MUST be disabled when `CI=true` or `NO_TELEMETRY=1` (or `TOOLNAME_NO_TELEMETRY=1`) is set
4. **Time-bounded** — if telemetry runs in a background thread/process, it MUST be abandoned after a short deadline (≤500ms) so the process can exit

Agents calling tools in loops cannot tolerate per-call telemetry latency. A tool with 100ms synchronous analytics per call costs 50 seconds of dead time per 500-call session.

## Acceptance Criteria

- `time tool list` in a network-isolated environment completes in the same time as `time tool list` with full network access (within 50ms)
- A telemetry endpoint that times out does not delay tool exit by more than 500ms
- With `CI=true`, no outbound network connections are made to telemetry endpoints
- Telemetry failure produces no output on stdout or stderr and does not change the exit code
- `strace -e trace=network tool list` with `CI=true` shows no telemetry-related syscalls

---

## Schema

No dedicated schema type

---

## Wire Format

No wire format — telemetry is a background side channel with no stdout/stderr presence

---

## Example

```
$ CI=true time tool list
{"ok":true,"data":[...]}
real    0m0.043s   ← no telemetry delay

$ time tool list    # with telemetry enabled
{"ok":true,"data":[...]}
real    0m0.045s   ← telemetry is fire-and-forget, process exits immediately
```

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-008](f-008-no-color-and-ci-environment-detection.md) | F | Provides: CI detection that triggers telemetry suppression |
| [REQ-F-029](f-029-auto-update-suppression-in-non-interactive-mode.md) | F | Extends: update checks follow same non-blocking contract |
| [REQ-F-050](f-050-update-notifier-side-channel-suppression.md) | F | Specializes: update notifier is a specific case of telemetry side-channel |
