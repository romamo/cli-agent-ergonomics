# jpoehnelt / agent-dx-cli-scale

> A scoring rubric and design pattern for evaluating CLI agent-readiness
> GitHub: https://github.com/jpoehnelt/skills/blob/main/agent-dx-cli-scale/SKILL.md
> Type: Design framework / evaluation rubric (not a code library)
> Author: Justin Poehnelt (Google Developer Relations)

---

## Overview

agent-dx-cli-scale is not a CLI framework — it is an **evaluation rubric and design philosophy** for measuring how well an existing CLI is designed for AI agent consumption. It defines a 7-axis scoring system (0–3 per axis, 0–21 total) that grades CLIs on agent-readiness, plus a "Multi-Surface Readiness" bonus checklist.

The rubric is published as a Claude Code skill (SKILL.md with YAML frontmatter), meaning it is designed to be loaded into an AI agent's context at conversation start so the agent can apply it to evaluate any CLI the user mentions.

The companion blog post (referenced in the SKILL.md) is "Rewrite Your CLI for AI Agents" and articulates the underlying philosophy: *"Human DX optimizes for discoverability and forgiveness. Agent DX optimizes for predictability and defense-in-depth."*

---

## Architecture & Design

**Format:** SKILL.md — YAML frontmatter + Markdown scoring table
**Deployment:** Loaded into Claude Code (or similar agent) as a context skill
**Scope:** Evaluation tool, not implementation framework

**The 7 Scoring Axes:**

### Axis 1: Machine-Readable Output (0–3)
- 0: Human-only output (tables, color codes, prose)
- 1: `--output json` exists but incomplete/inconsistent
- 2: Consistent JSON output + errors also return structured JSON
- 3: NDJSON streaming for pagination; structured output default in non-TTY

### Axis 2: Raw Payload Input (0–3)
- 0: Only bespoke flags
- 1: `--json` or stdin JSON for some commands
- 2: All mutating commands accept raw JSON payload mapping to API schema
- 3: Raw payload is first-class; agent uses API schema as documentation with zero translation loss

### Axis 3: Schema Introspection (0–3)
- 0: Only `--help` text
- 1: `--help --json` or `describe` for some commands
- 2: Full schema introspection for all commands as JSON
- 3: Live runtime-resolved schemas from discovery document; includes scopes, enums, nested types

### Axis 4: Context Window Discipline (0–3)
- 0: Full API responses, no field limiting
- 1: `--fields` on some commands
- 2: Field masks on all read commands; pagination with `--page-all`
- 3: Streaming pagination (NDJSON per page); explicit skill guidance on field mask usage

### Axis 5: Input Hardening (0–3)
- 0: No validation beyond basic type checks
- 1: Some validation; does not cover agent hallucination patterns
- 2: Rejects path traversals (`../`), percent-encoded segments, embedded query params
- 3: All of above + output path sandboxing, HTTP-layer encoding, explicit security posture ("agent is not trusted operator")

### Axis 6: Safety Rails (0–3)
- 0: No dry-run, no response sanitization
- 1: `--dry-run` for some mutating commands
- 2: `--dry-run` for all mutating commands
- 3: Dry-run + response sanitization (e.g., Model Armor) against prompt injection in API data

### Axis 7: Agent Knowledge Packaging (0–3)
- 0: Only `--help` and docs site
- 1: `CONTEXT.md` or `AGENTS.md` with basic guidance
- 2: Structured skill files (YAML + Markdown) per command/surface
- 3: Comprehensive skill library with agent-specific guardrails; skills versioned, discoverable, follow a standard like OpenClaw

**Rating bands:**
- 0–5: Human-only
- 6–10: Agent-tolerant
- 11–15: Agent-ready
- 16–21: Agent-first

**Bonus: Multi-Surface Readiness**
- MCP (stdio JSON-RPC) — typed tool invocation, no shell escaping
- Extension/plugin install — agent treats CLI as native capability
- Headless auth — env vars for tokens, no browser redirect

---

## Agent Compatibility Assessment

### What it handles natively

As an evaluation tool rather than a framework, it "handles" challenges by *defining* what good looks like:

- **Output Format & Parseability** — Axis 1 directly addresses this; defines levels from human-only to NDJSON streaming
- **Schema & Help Discoverability** — Axis 3 defines the spectrum from `--help` text to live runtime schema
- **Verbosity & Token Cost** — Axis 4 "Context Window Discipline" is explicitly token-aware
- **Argument Validation / Input Hardening** — Axis 5 goes beyond standard validation to agent-specific hallucination patterns (path traversal, percent-encoding, embedded query params)
- **Side Effects & Destructive Operations** — Axis 6 Safety Rails directly addresses dry-run
- **Prompt Injection via Output** — Axis 6 level 3 explicitly mentions response sanitization (Model Armor)
- **Command Composition / Raw Payload** — Axis 2 addresses agents passing structured JSON directly

### What it handles partially

- **Interactivity** — not explicitly scored, though Axis 2 (raw payload input) partially addresses it
- **Error Message Quality** — implied by Axis 1 (errors return structured JSON at level 2+) but not a dedicated axis
- **Authentication** — mentioned in bonus checklist (headless auth) but not scored

### What it does not handle

As an evaluation rubric it does not implement anything. For implementation gaps it does not *measure*:
- Exit codes (no axis for exit code taxonomy)
- Timeouts and hanging processes
- Idempotency and safe retries
- Partial failure and atomicity
- Signal handling
- Child process leakage
- Encoding safety
- Observability / audit trail
- Config shadowing
- Race conditions
- Network proxy awareness
- Self-update behavior

---

## Challenge Coverage Table

| # | Challenge | Rating | Reason |
|---|-----------|--------|--------|
| 1 | Exit Codes & Status Signaling | ✗ | No scoring axis for exit codes |
| 2 | Output Format & Parseability | ✓ | Axis 1 directly covers this with 4 levels |
| 3 | Stderr vs Stdout Discipline | ✗ | Not measured |
| 4 | Verbosity & Token Cost | ✓ | Axis 4 "Context Window Discipline" explicitly |
| 5 | Pagination & Large Output | ✓ | Axis 4 level 3 covers NDJSON streaming pagination |
| 6 | Command Composition & Piping | ~ | Axis 2 (raw payload) partially covers composition |
| 7 | Output Non-Determinism | ✗ | Not measured |
| 8 | ANSI & Color Code Leakage | ~ | Implied by Axis 1 level 0 ("color codes" = bad) |
| 9 | Binary & Encoding Safety | ✗ | Not measured |
| 10 | Interactivity & TTY Requirements | ✗ | Not a scored axis |
| 11 | Timeouts & Hanging Processes | ✗ | Not measured |
| 12 | Idempotency & Safe Retries | ✗ | Not measured |
| 13 | Partial Failure & Atomicity | ✗ | Not measured |
| 14 | Argument Validation Before Side Effects | ~ | Axis 5 covers validation but not phase ordering |
| 15 | Race Conditions & Concurrency | ✗ | Not measured |
| 16 | Signal Handling & Graceful Cancellation | ✗ | Not measured |
| 17 | Child Process Leakage | ✗ | Not measured |
| 18 | Error Message Quality | ~ | Axis 1 level 2 requires structured JSON errors |
| 19 | Retry Hints in Error Responses | ✗ | Not measured |
| 20 | Environment & Dependency Discovery | ✗ | Not measured |
| 21 | Schema & Help Discoverability | ✓ | Axis 3 directly covers this with 4 levels |
| 22 | Schema Versioning & Output Stability | ~ | Axis 3 level 3 mentions "current API version" |
| 23 | Side Effects & Destructive Operations | ✓ | Axis 6 Safety Rails directly covers dry-run |
| 24 | Authentication & Secret Handling | ~ | Bonus checklist mentions headless auth |
| 25 | Prompt Injection via Output | ✓ | Axis 6 level 3 explicitly covers response sanitization |
| 26 | Stateful Commands & Session Management | ✗ | Not measured |
| 27 | Platform & Shell Portability | ✗ | Not measured |
| 28 | Config File Shadowing & Precedence | ✗ | Not measured |
| 29 | Working Directory Sensitivity | ✗ | Not measured |
| 30 | Undeclared Filesystem Side Effects | ✗ | Not measured |
| 31 | Network Proxy Unawareness | ✗ | Not measured |
| 32 | Self-Update & Auto-Upgrade Behavior | ✗ | Not measured |
| 33 | Observability & Audit Trail | ✗ | Not measured |

**Summary: ✓ 6 / ~ 6 / ✗ 21**

---

## Unique Contributions Not in Other Frameworks

**1. Agent-specific input hardening (Axis 5)**
The rubric explicitly names agent hallucination patterns as distinct from human typos:
- Path traversals (`../`)
- Percent-encoded segments (`%2e`)
- Embedded query params (`?`, `#` in resource IDs)
- Security posture: *"The agent is not a trusted operator"*

This is a unique and important insight absent from all other frameworks reviewed.

**2. Knowledge packaging as a scored axis (Axis 7)**
Explicitly scores whether a CLI ships agent-consumable skill files, CONTEXT.md, or a structured skill library. No other framework treats this as a first-class concern.

**3. Multi-surface readiness**
Frames MCP, plugin install, and headless auth as complementary surfaces for the same CLI — not alternatives. A CLI should support all three simultaneously.

**4. The "translation loss" framing (Axis 2)**
Level 3 of raw payload input frames the goal as "zero translation loss" between the API schema and what the agent passes — the agent should be able to use the API schema as documentation directly. This is a precise and actionable design target.

---

## Strengths for Agent Use

1. **Conceptual clarity** — the clearest articulation of agent-vs-human DX tradeoffs of any resource reviewed
2. **Input hardening taxonomy** — unique focus on agent-specific attack/failure vectors (hallucinations, not typos)
3. **Knowledge packaging** — the only framework that treats shipping agent skill files as a first-class design requirement
4. **Practical scoring** — immediately applicable to audit any existing CLI for agent readiness
5. **Prompt injection addressed** — one of the few references to call out response sanitization explicitly

## Weaknesses for Agent Use

1. **Not a code framework** — scores CLIs but provides no implementation
2. **7 axes miss 26 of 33 challenges** — exit codes, timeouts, signals, idempotency, observability, and more are unscored
3. **No acceptance criteria** — scoring bands are qualitative; two evaluators may score the same CLI differently
4. **Static skill file** — the rubric itself is not versioned or discoverable by agents at runtime

## Verdict

agent-dx-cli-scale is the most conceptually sophisticated artifact in this review — not as a framework but as a design philosophy. Its framing of "agent is not a trusted operator," its explicit treatment of hallucination-specific input hardening, and its unique Axis 7 (knowledge packaging) contribute ideas that no other framework has articulated. As a scoring rubric it covers 12 of 33 challenges at least partially. Its primary limitation is that it evaluates rather than implements — it tells you what score your CLI has, not how to fix it. Used together with agentyper or as the design spec for a new framework, it provides invaluable conceptual grounding.
