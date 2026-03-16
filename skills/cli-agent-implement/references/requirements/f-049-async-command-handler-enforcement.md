# REQ-F-049: Async Command Handler Enforcement

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§40 `parse()` vs `parseAsync()` Silent Race Condition](../challenges/01-critical-ecosystem-runtime-agent-specific/40-high-async-race-condition.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

The framework MUST execute all command handlers as async functions within a managed async event loop. The framework MUST reject synchronous command handlers at registration time (or emit a deprecation error). The framework MUST ensure that async operations within command handlers are fully awaited before the process exits. The framework MUST NOT call `process.exit()` (Node.js) or `sys.exit()` (Python) until all async command handlers and their registered cleanup hooks have resolved. Partial async execution that leads to silent data loss is a framework-level defect.

## Acceptance Criteria

- A command handler defined as a sync function produces a framework registration warning/error.
- An async operation started but not awaited within a command handler is detected by the framework's async completion check.
- `process.exit(0)` is called only after all async command teardown hooks have resolved.
- A command that performs async I/O completes all writes before exiting.
