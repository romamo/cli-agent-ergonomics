> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §65

## 65. Global Configuration State Contamination

**Source:** Antigravity `04_state_and_concurrency.md` (RA)

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Medium | **Time:** High | **Context:** Low

### The Problem

Distinct from §28 (config file shadowing on READ), this challenge is about tools that WRITE to global configuration files (`~/.config/tool/`, `~/.tool/config.json`) as a side effect of normal operations, permanently altering the host environment for all future sessions. An agent running `tool configure --region us-east-1` intending a per-task setting may inadvertently persist it to the user's global config, affecting every subsequent human and agent session on that machine.

```bash
# Agent sets a config value, intending it to be temporary for this task
$ tool config set output-format=json
# Tool writes to ~/.config/tool/config.json
# Every future invocation of this tool by any user now outputs JSON
# Human opens a new terminal: tool behaves differently — agent contaminated the env

# More dangerous: agent changes authentication context
$ tool auth switch --account staging-account
# Tool writes active account to ~/.tool/auth.json
# Human's next tool use is unexpectedly in staging account — data risk

# Auto-migration contaminates even without explicit config commands:
$ tool update
# New version runs, silently migrates ~/.config/tool/config.json schema
# Git status now shows unexpected modifications — confusing to human
```

### Impact

- Permanent environmental changes visible to all users and future sessions
- Humans return to a modified environment after agent session — confusing and potentially dangerous
- CI systems share a filesystem; one agent job contaminates config for subsequent jobs
- Auto-migration writes make git working trees unexpectedly dirty

### Solutions

**Default all writes to local/session scope:**
```bash
# Bad: writes to global ~/.config/tool/config.json
$ tool config set region=us-east-1

# Good: writes to ./.tool-config (local, git-ignorable)
$ tool config set region=us-east-1
# Requires explicit --global flag for home-dir writes:
$ tool config set --global region=us-east-1
```

**Strict scope declaration in schema:**
```json
{
  "name": "config set",
  "write_scope": "local",   // "local" | "global" | "session"
  "global_flag": "--global",
  "danger_level": "mutating"
}
```

**Config write audit trail:**
```json
{
  "ok": true,
  "warnings": [
    {
      "code": "GLOBAL_CONFIG_MODIFIED",
      "path": "~/.config/tool/config.json",
      "key": "region",
      "previous_value": "eu-west-1",
      "new_value": "us-east-1"
    }
  ]
}
```

**For framework design:**
- Framework MUST default all config writes to the nearest `.tool-config` file in the working directory hierarchy, not to `~/.config/`.
- Global config writes MUST require an explicit `--global` flag and MUST emit a `GLOBAL_CONFIG_MODIFIED` warning in the JSON response.
- Auto-migrations MUST be opt-in: `tool migrate-config --confirm` rather than running silently on startup.
