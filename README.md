# CLI Agent Ergonomics

A specification for building CLI tools that work reliably under AI agent orchestration.

Most CLI tools are designed for humans. They use exit code `1` for everything, write mixed content to stdout, prompt for input, paginate output, and emit ANSI color codes. An AI agent calling these tools wastes tokens parsing error messages, enters retry loops on ambiguous failures, and silently proceeds after operations that partially succeeded. This specification defines the contracts a CLI tool or framework must satisfy to eliminate these failure modes.

---

## What's in this repo

| Path | Contents |
|------|----------|
| [`challenges/`](challenges/index.md) | 65 failure modes grouped into 7 parts, each with severity, frequency, and agent impact |
| [`requirements/`](requirements/index.md) | 133 requirements across 3 tiers that address the challenges |
| [`schemas/`](schemas/index.md) | JSON Schema definitions for exit codes, response envelopes, and the tool manifest |
| [`comparison-matrix.md`](comparison-matrix.md) | How 12 existing frameworks (argparse, click, cobra, clap, …) cover the 65 challenges |

---

## The 65 challenges

Grouped into 7 parts by category:

| Part | Challenges | Focus |
|------|-----------|-------|
| 1 | 32 | Ecosystem, runtime, agent-specific patterns |
| 2 | 9 | Execution and reliability |
| 3 | 4 | Security |
| 4 | 8 | Output and parsing |
| 5 | 5 | Environment and state |
| 6 | 6 | Errors and discoverability |
| 7 | 1 | Observability |

Each challenge documents: severity, frequency, detectability, token spend, time cost, and context cost — from the agent's perspective.

---

## The 133 requirements

Three tiers, implemented in order:

| Tier | Count | Meaning |
|------|-------|---------|
| **F** — Framework-Automatic | 66 | Enforced by the framework without command author action |
| **C** — Command Contract | 26 | Declared by the command author at registration |
| **O** — Opt-In | 41 | Explicitly enabled by the application |

Start with the P0 Framework requirements — they establish the exit code table, response envelope, and validation phase boundary that everything else depends on.

---

## Key contracts

**Exit codes** — 14 named codes (0–13) covering every standard condition. Each carries machine-readable guarantees: whether the operation is retryable and how far side effects progressed. Commands declare every code they may emit at registration time. See [`exit-code.json`](schemas/exit-code.json).

**Response envelope** — every command output is wrapped in `{ ok, data, error, warnings, meta }`. The same keys are always present regardless of success, failure, or result count. See [`response-envelope.json`](schemas/response-envelope.json).

**Tool manifest** — a single `tool manifest` command returns the complete command tree as JSON: every subcommand, flag, type, description, exit code, and example. Agents can construct valid calls without iterating `--help` across every subcommand. See [`manifest-response.json`](schemas/manifest-response.json).

---

## For implementers

If you are implementing this specification in a CLI framework or tool, read [`IMPLEMENTING.md`](IMPLEMENTING.md). It covers:

- Requirement tier order (F → C → O)
- How to read a requirement file
- Generating language-specific types from the schemas (Python, TypeScript, Rust, Go, Java)
- Key invariants that code generators do not enforce
- Suggested implementation order

---

## For AI agents

- **Implementing the spec:** read [`IMPLEMENTING.md`](IMPLEMENTING.md)
- **Editing the spec:** read [`AGENTS.md`](AGENTS.md)

---

## For spec editors

[`AGENTS.md`](AGENTS.md) defines all conventions for adding or updating challenges, requirements, and schemas: file naming, required sections, styling rules, and cross-reference format.

To validate cross-links after any edit, use the `/validate-links` skill (Claude Code) or run the scripts in `.claude/skills/validate-links/SKILL.md` directly.
