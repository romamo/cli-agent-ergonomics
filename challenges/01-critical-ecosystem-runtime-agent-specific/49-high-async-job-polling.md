> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §49

## 49. Async Job / Polling Protocol Absence

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Medium

### The Problem

Many CLI operations are inherently asynchronous — deployments, builds, data migrations, batch exports. Tools handle this in two broken ways: (a) block synchronously until completion, consuming the agent's entire timeout budget with no progress signal, or (b) return a job ID immediately with no documented machine-readable protocol for status polling, interpreting completion states, or cancellation.

```bash
# Pattern A: blocks silently until done (or forever)
$ tool deploy --env prod
# ... hangs for 8 minutes with no output ...
# Agent's timeout fires; tool killed mid-deploy; partial state

# Pattern B: returns job ID but protocol is undocumented
$ tool deploy --env prod --async
Job started: dep_abc123
$ echo $?
0   # exit 0 means... "job submitted" or "job done"?

$ tool job status dep_abc123
Running... (60%)
$ echo $?
0   # exit 0 means "query succeeded" or "job completed"?
# Agent cannot distinguish "still running" from "done"
```

Compound failure: agent must guess the polling interval, doesn't know the maximum wait time, and has no way to cancel a runaway job once started.

### Impact

- Agent burns entire timeout budget on synchronous jobs
- Agent misreads `exit 0` from a status query as job completion, proceeds prematurely
- Agent has no cancellation path for a runaway job
- Job IDs may not be valid across sessions; no way to resume a disrupted poll loop

### Solutions

**Async commands MUST return a typed job descriptor:**
```json
{
  "ok": true,
  "data": {
    "job_id": "dep_abc123",
    "status": "running",
    "terminal": false,
    "status_command": "tool job status dep_abc123",
    "cancel_command": "tool job cancel dep_abc123",
    "poll_interval_ms": 5000,
    "timeout_ms": 600000,
    "started_at": "2024-03-11T14:00:00Z"
  }
}
```

**Status command uses distinct exit codes:**
```
exit 0  = job complete (terminal, success)
exit 3  = job still running (non-terminal, poll again)
exit 4  = job failed (terminal, failure)
exit 7  = job timed out (terminal)
exit 5  = job ID not found / expired
```

**Terminal vs non-terminal distinction in response:**
```json
{ "status": "running", "terminal": false, "progress_pct": 60 }
{ "status": "complete", "terminal": true, "result": {...} }
```

**For framework design:**
- Provide a first-class `AsyncJob` return type; framework automatically generates `job status <id>` and `job cancel <id>` subcommands.
- The job descriptor schema (status_command, cancel_command, poll_interval_ms, timeout_ms) must be part of the standard response envelope for any async operation.
- Document the exit code contract for status commands prominently as part of the framework's standard.
