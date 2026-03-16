# REQ-C-022: Async Commands Declare Job Descriptor Schema

**Tier:** Command Contract | **Priority:** P0

**Source:** [§49 Async Job / Polling Protocol Absence](../challenges/01-critical-ecosystem-runtime-agent-specific/49-high-async-job-polling.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

Any command that initiates an asynchronous operation (one that does not complete before the process exits) MUST declare `async: true` in its registration metadata and MUST return a typed job descriptor in `data`. The job descriptor MUST include: `job_id`, `status` (`running`|`complete`|`failed`|`cancelled`), `terminal` (boolean), `status_command` (exact invocation to check status), `cancel_command` (exact invocation to cancel), `poll_interval_ms`, and `timeout_ms`. The framework auto-generates `job status <id>` and `job cancel <id>` subcommands for all registered async commands.

## Acceptance Criteria

- An async command's `--schema` output includes `async: true` and the job descriptor schema.
- The job descriptor returned at invocation time includes all required fields.
- `tool job status <id>` exits 0 for complete, 3 for still-running, 4 for failed, 5 for not-found.
- Attempting to register an async command without a job descriptor schema raises a framework error.
