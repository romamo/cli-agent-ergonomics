# REQ-F-046: Pager Environment Variable Suppression

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§10 Interactivity & TTY Requirements](../challenges/02-critical-execution-and-reliability/10-critical-interactivity.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

In addition to the pager suppression in REQ-F-010, the framework MUST set the following environment variables before any subprocess invocation to prevent third-party libraries from spawning interactive pagers: `PAGER=cat`, `GIT_PAGER=cat`, `LESS=-F -X -R`, `MORE= ` (empty), `MANPAGER=cat`. These variables MUST be set in the subprocess environment unconditionally when the framework's subprocess API is used, regardless of any inherited environment. Framework-level help rendering MUST also respect these settings.

## Acceptance Criteria

- A subprocess invoked via the framework API cannot open an interactive pager even if the host `PAGER` env var is set to `less`.
- `git log` invoked via the framework API does not block waiting for pager input in non-TTY mode.
- The environment variable injection is applied to all levels of subprocess nesting (direct children and grandchildren of the framework process).
- The suppression is transparent to command authors: no per-command configuration required.
