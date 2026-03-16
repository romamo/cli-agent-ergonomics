# REQ-F-031: SIGTERM Forwarding to Tracked Children

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§17 Child Process Leakage](../challenges/02-critical-execution-and-reliability/17-medium-child-process-leakage.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Low

---

## Description

The framework's SIGTERM handler (REQ-F-013) MUST forward `SIGTERM` to all children tracked in the session before emitting the cancellation JSON and exiting. The framework MUST wait up to a configurable grace period for children to exit before sending `SIGKILL`.

## Acceptance Criteria

- A child process registered with the framework receives `SIGTERM` when the parent receives `SIGTERM`.
- If a child does not exit within the grace period, the framework sends `SIGKILL` to that child.
- The parent's cancellation JSON output is emitted after children have been signaled.
