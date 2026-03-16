# Security

> Destructive operations, authentication, secret handling, and prompt injection.

**Challenges:** 3 active &nbsp;|&nbsp; 🔴 3 critical

---

| File | Severity | Summary |
|------|----------|---------|
| [23-critical-destructive-ops.md](23-critical-destructive-ops.md) | 🔴 Critical | Agents may execute destructive commands without fully understanding consequences, especially when operating autonomou... |
| [24-critical-auth-secrets.md](24-critical-auth-secrets.md) | 🔴 Critical | CLI tools often need credentials |
| [25-critical-prompt-injection.md](25-critical-prompt-injection.md) | 🔴 Critical | CLI tool output is fed directly into the agent's context |

## Detailed Metrics

| Challenge | Severity | Frequency | Detectability | Token Spend | Time | Context |
|-----------|----------|-----------|---------------|-------------|------|---------|
| [§23](23-critical-destructive-ops.md) | 🔴 Critical | Common | Medium | Medium | High | Medium |
| [§24](24-critical-auth-secrets.md) | 🔴 Critical | Common | Hard | Medium | Medium | Low |
| [§25](25-critical-prompt-injection.md) | 🔴 Critical | Situational | Hard | High | High | High |
