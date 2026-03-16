> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §44

## 44. Agent Knowledge Packaging Absence

**Severity:** Medium | **Frequency:** Very Common | **Detectability:** Easy | **Token Spend:** High | **Time:** High | **Context:** Medium

### The Problem

Agents consuming a CLI tool have two information sources: the tool's `--help` text (or `--schema` if available) and any contextual documentation. JSON Schema describes *what* arguments a tool accepts; it cannot describe *when* to use it, *what order* to run commands in, *which combinations are dangerous*, or *what the known gotchas are* in the specific deployment environment.

The absence of agent-facing documentation (AGENTS.md, CONTEXT.md, skill files) means agents must rely on:
1. General training knowledge about the tool (often outdated or wrong for non-default configurations)
2. Trial-and-error (expensive in tokens, time, and potential side effects)
3. Inferring behavioral constraints from `--help` text that was written for human readers

The jpoehnelt rubric makes this a scored axis (Axis 7), with four levels ranging from "only --help" (score 0) to "comprehensive skill library with versioned, discoverable skill files" (score 3). No other framework or specification in the research treats agent knowledge packaging as a first-class concern.

Specifically absent from most tools:
- Which subcommand to use for a given task ("use `user invite`, not `user create`")
- What must be set up before the tool will work ("requires `auth login` to have been run")
- Which flags are dangerous and require `--dry-run` first
- Common error patterns and their solutions
- Rate limits and retry guidance specific to this tool
- The difference between staging and production behavior

```markdown
# Example: a tool with a known gotcha, but no AGENTS.md
$ my-tool deploy --env production
Error: invalid token  # What token? Which env var? Why now?
# Agent retries with different args, can't find solution
# Human: "Oh, you need to run `my-tool auth refresh` first after 8 hours"
# This is not in --help; it's not in the schema; only in an internal wiki
```

### Impact

- Agent fails silently on tasks it could complete with appropriate context.
- Agents make dangerous operations without understanding that `--dry-run` should be run first.
- Significant token spend on trial-and-error exploration of tool behavior.
- Agents learn incorrect generalizations from failed invocations (e.g., "this tool requires `--force` to work" when the real issue was a missing prerequisite).
- Knowledge locked in human documentation (READMEs, wikis, runbooks) is invisible to agents.
- Without versioned skill files, agents may use outdated guidance after tool updates.

### Solutions

**Minimum viable AGENTS.md:**
```markdown
# AGENTS.md

## Quick Reference
- Deploy: `my-tool deploy --env <staging|production> --dry-run` (always dry-run first)
- Auth: `my-tool auth login` must be run before any other command; tokens expire in 8 hours
- Status check: `my-tool status --json` returns current system health

## Known Gotchas
- If you see "invalid token", run `my-tool auth refresh` (tokens expire every 8 hours)
- `deploy` to production requires `--confirm` flag; staging does not
- The `--region` flag defaults to us-east-1 in CI, eu-west-1 locally

## Safe Operations
Read-only: `list`, `get`, `status`, `logs`
Mutating: `deploy`, `delete`, `update` (run with --dry-run first)
Irreversible: `delete --permanent` (no dry-run available)
```

**OpenClaw skill file with machine-readable metadata:**
```yaml
---
name: my-tool
version: "1.0.0"
triggers:
  - "deploy to production"
  - "my-tool"
tools: [bash]
---
[Skill body with agent-specific guidance]
```

**For framework design:**
- Auto-generate a minimal AGENTS.md template from schema metadata at `my-tool --generate-agents-md`.
- Include in `--schema` output: `"danger_level"`, `"requires"` (prerequisite commands), `"read_only"`, and `"docs_url"` fields.
- Provide a CLI hook to load and display skill files: `my-tool --skill` returns the tool's OpenClaw skill.
- Score frameworks against Axis 7 and require at least level 1 (CONTEXT.md or AGENTS.md present) before an "agent-ready" designation.
