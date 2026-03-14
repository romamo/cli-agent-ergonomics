# REQ-O-034: tool generate-skills Built-In Command

**Tier:** Opt-In | **Priority:** P2

**Source:** [§44 Agent Knowledge Packaging Absence](../challenges/01-critical-ecosystem-runtime-agent-specific/44-medium-knowledge-packaging.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: High

---

## Description

The framework MUST provide a built-in `tool generate-skills` command that generates agent-consumable skill files from the registered command schemas. The command MUST produce: one `CONTEXT.md` file with a high-level overview of the tool, its commands, and agent-specific guidance; and one `SKILL-<command>.md` file per command with YAML frontmatter (name, description, version, args schema) and Markdown body (usage examples, guardrails, common patterns, anti-patterns). The output MUST be compatible with the OpenClaw skill format and loadable as Claude Code skills. The command MUST support `--output-dir <path>` and `--format <markdown|json>`.

## Acceptance Criteria

- `tool generate-skills --output-dir ./skills` creates `CONTEXT.md` and one `SKILL-*.md` per command.
- Each skill file includes a YAML frontmatter block with command name, description, and argument schema.
- Each skill file includes at least three example invocations derived from the command's `--schema` output.
- The generated files pass validation by an OpenClaw-compatible skill loader.
