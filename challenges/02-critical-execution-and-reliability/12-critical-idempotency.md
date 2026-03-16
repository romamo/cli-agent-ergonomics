> **Part II: Execution & Reliability** | Challenge §12

## 12. Idempotency & Safe Retries

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Medium

### The Problem

Agents retry on failure. If a command is not idempotent, retries cause duplicated side effects: double payments, duplicate records, multiple emails sent.

**Non-idempotent operations agents commonly retry:**
```bash
$ tool send-email --to user@example.com --subject "Welcome"
# Network timeout after sending
# Agent retries → duplicate email sent

$ tool create-order --amount 100
# Returns 503, agent retries → two orders created

$ tool increment-counter --key views
# Flaky network, agent retries 3x → counter incremented 3x
```

**Idempotency that's not communicated:**
```bash
$ tool deploy --version 1.2.3
# First run: deploys
# Second run: no-op (already at 1.2.3)
# But exits 0 both times with identical output
# Agent cannot tell if it deployed or was already up-to-date
```

### Impact

- Duplicate financial transactions, messages, records
- Agent cannot safely resume after failure
- State becomes inconsistent, hard to recover

### Solutions

**Idempotency keys:**
```bash
tool create-order --amount 100 --idempotency-key "order-$(date +%s)-$RANDOM"
# Server deduplicates based on key
# Safe to retry indefinitely
```

**Declare operation effect in output:**
```json
{
  "ok": true,
  "effect": "created",        // "created" | "updated" | "noop" | "deleted"
  "data": {"id": 42}
}
```

```json
{
  "ok": true,
  "effect": "noop",
  "reason": "Already at version 1.2.3",
  "data": {"current_version": "1.2.3"}
}
```

**`--dry-run` flag for all mutating commands:**
```bash
tool deploy --version 1.2.3 --dry-run
# Output:
{
  "ok": true,
  "effect": "would_create",
  "changes": ["would update service to 1.2.3", "would restart 2 instances"]
}
```

**For framework design:**
- Mark commands as `safe` (read-only, always idempotent) or `unsafe` (mutating)
- Require `--idempotency-key` for all `unsafe` commands, or generate one automatically
- Emit `effect` field in all responses
- Implement `--dry-run` as a framework-level feature, not per-command
