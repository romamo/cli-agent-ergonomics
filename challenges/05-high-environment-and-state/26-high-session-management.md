> **Part V: Environment & State** | Challenge §26

## 26. Stateful Commands & Session Management

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

Some CLIs maintain state between invocations (login sessions, active contexts, selected environments). Agents running commands in parallel or across sessions can have state conflicts.

**Hidden global state:**
```bash
$ tool use-context production
Switched to production context.

# In another agent session simultaneously:
$ tool use-context staging
Switched to staging context.

# Back in first session:
$ tool deploy   # ← now deploys to staging, not production!
```

**Session state without indication:**
```bash
$ tool login
Logged in as alice@example.com

$ tool list-resources
# Returns resources for alice — but agent doesn't know it's logged in as alice
# If another process ran `tool login` as bob, results changed silently
```

**State stored in shared locations:**
```bash
~/.config/tool/current-context   # shared across all processes, all agents
```

### Solutions

**Explicit context per invocation:**
```bash
tool deploy --context production           # never rely on implicit current context
tool list-resources --token $TOKEN         # stateless auth per-call
tool --config /tmp/agent-session-42.json deploy  # isolated config file
```

**State inspection command:**
```bash
$ tool status --output json
{
  "logged_in": true,
  "user": "alice@example.com",
  "current_context": "production",
  "token_expires": "2024-03-11T16:00:00Z"
}
```

**For framework design:**
- Provide `--config` / `--context` override for every command
- Default to stateless operation; state is opt-in
- Document all global state locations in `tool status --show-state-files`
