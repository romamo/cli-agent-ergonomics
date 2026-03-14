# AGENTS.md — Spec Editor Guide for AI Agents

This file is for AI agents helping to **maintain and extend the specification** — adding challenges, requirements, and schemas. It defines conventions every editor agent must follow.

If you are helping someone **implement** this specification in their own project, read [`IMPLEMENTING.md`](IMPLEMENTING.md) instead.

---

## Project overview

This project defines the **CLI Agent Ergonomics** specification: a catalogue of challenges, requirements, shared schemas, and a comparison matrix for building CLI tools that work reliably under AI agent orchestration.

---

## Directory structure

```
AGENTS.md                   ← spec editor guide (this file)
IMPLEMENTING.md             ← implementer guide for AI agents
comparison-matrix.md        ← solution comparison across all 65 challenges
challenges/                 ← 65 challenges grouped into 7 parts
  index.md                  ← master index of all challenges
  sources.md                ← source evidence for each challenge
  checklist.md              ← implementation checklist
  01-critical-ecosystem-runtime-agent-specific/
  02-critical-execution-and-reliability/
  03-critical-security/
  04-critical-output-and-parsing/
  05-high-environment-and-state/
  06-high-errors-and-discoverability/
  07-medium-observability/
requirements/               ← 133 requirements across 3 tiers
  index.md                  ← master index of all requirements
  f-NNN-<slug>.md           ← REQ-F: Framework-Automatic
  c-NNN-<slug>.md           ← REQ-C: Command Contract
  o-NNN-<slug>.md           ← REQ-O: Opt-In
schemas/                    ← canonical JSON Schema definitions
  index.md                  ← schema directory and codegen quick-reference
  codegen-guide.md          ← full installation + generation guide for all languages
  <name>.json               ← machine-consumable schema (source of truth)
  <name>.md                 ← human-readable companion: field table + implementation notes
```

---

## Styling rules

These rules apply to **all documents** in this project. Apply them when creating or updating any file.

### 1. No trailing periods in lists, tables, or cells

Sentences placed inside a list item, table cell, or blockquote cell MUST NOT end with a period.

**Correct**
```markdown
- Validation failed before execution began
- Safe to retry unconditionally after fixing the input

| Field  | Description              |
|--------|--------------------------|
| `code` | Stable machine-readable identifier |
```

**Incorrect**
```markdown
- Validation failed before execution began.
- Safe to retry unconditionally after fixing the input.

| Field  | Description                         |
|--------|-------------------------------------|
| `code` | Stable machine-readable identifier. |
```

Periods are only used to end sentences in **prose paragraphs** (Description, Purpose, Implementation notes body text).

### 2. Inline code for all identifiers

Flag names, field names, constants, file names, command invocations, and schema `$id` values must be wrapped in backticks.

**Correct:** `exit_codes` · `ExitCode.NOT_FOUND` · `--schema` · `error.redirect.command`
**Incorrect:** exit_codes · ExitCode.NOT_FOUND · --schema

### 3. Verb-first relationship labels in Related tables

Every row in a `## Related` table must start with a verb describing the relationship direction.

Allowed verbs: `Provides` · `Consumes` · `Enforces` · `Specializes` · `Composes` · `Aggregates` · `Wraps` · `Sources` · `Exposes` · `Extends`

### 4. Present tense in descriptions

All `description` fields (in schemas, requirement files, and table cells) use present tense.

**Correct:** `"Operation completed as intended"`
**Incorrect:** `"Operation will complete as intended"` / `"Operation has completed"`

### 5. Agent-readable `description` fields

Descriptions in `ExitCodeEntry`, `FlagEntry`, and `ErrorDetail` are read by agents at runtime. They must:
- State the condition, not the intent (`"Target cluster not found"` not `"Finds the target cluster"`)
- Be ≤ 120 characters
- Not end with a period

---

## Challenge files

**Naming:** `{nn:02d}-{severity}-{slug}.md` inside the matching part folder

**Severity order within a part:** critical → high → medium

**Required frontmatter line** (first metadata line after the title):
```
**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** High | **Context:** Medium
```

When adding a challenge:
1. Assign the next available `§N` number
2. Place it in the correct part folder by severity
3. Add a row to `challenges/index.md` and the part's `index.md`
4. Add a row to `challenges/sources.md`
5. Create or update any requirements that address it

---

## Requirement files

**Naming:** `{tier}-{NNN}-{slug}.md` where tier is `f`, `c`, or `o`

**Tiers:**
- `f` — Framework-Automatic: enforced without command author action
- `c` — Command Contract: declared by the command author at registration
- `o` — Opt-In: explicitly enabled by the application

**Required sections in order:**
1. `## Description` — prose, may end sentences with periods
2. `## Acceptance Criteria` — bulleted list, no trailing periods
3. `## Schema` — links to `../schemas/<name>.json` using the filename as link text (e.g. `[exit-code.json](../schemas/exit-code.json)`), followed by requirement-specific constraints only
4. `## Wire Format` — JSON example of the output (if applicable)
5. `## Example` — unformatted pseudocode, language-agnostic
6. `## Related` — cross-reference table: `Requirement | Tier | Relationship`

When adding a requirement:
1. Assign the next `NNN` within the tier
2. Add a row to `requirements/index.md`
3. Link the related schema file(s) from `## Schema`
4. Add the requirement to the `Related` table of every schema it uses

---

## Schema files

Every shared type has two files: a `.json` (machine-consumable) and a `.md` (human-readable).

**`.json` file rules:**
- JSON Schema draft-07
- `$id` matches the file name without extension (e.g. `"$id": "ExitCode"`)
- All properties have a `description`
- Use `$ref` to reference other schemas by filename (e.g. `"$ref": "exit-code.json"`)
- No language-specific content

**`.md` file sections in order:**

| # | Section | Audience | Content |
|---|---------|----------|---------|
| 1 | Title + file link + Used by | everyone | Header, link to `.json`, requirement back-links |
| 2 | `## Purpose` | everyone | Why this type exists; key design decisions |
| 3 | `## Values` / field table | everyone | Enum table or field table with description and when-to-use; no trailing periods |
| 4 | `## Examples` | everyone | Valid instances, then invalid instances with violation named |
| 5 | `## Common mistakes` | human developers | What developers get wrong; bulleted list; no trailing periods |
| 6 | `## Agent interpretation` | runtime agents | Decision rules for consuming output: missing fields, contradictions, retry logic; no trailing periods |
| 7 | `## Coding agent notes` | AI coding assistants | Type representation, validation to generate, tests to generate, anti-patterns; no trailing periods |
| 8 | `## Implementation notes` | human developers | Prose rationale and edge cases; sentences may end with periods |

Sections 1–4 are read by all audiences. Sections 5–8 are audience-specific — each reader goes directly to their section after reading the shared baseline.

When adding a schema type:
1. Create `schemas/<name>.json` and `schemas/<name>.md`
2. Add a row to `schemas/index.md`
3. Reference the `.json` file from any requirement that uses the type

---

## Cross-reference conventions

- Challenges are referenced as `§N` (e.g. `§34`)
- Requirements are referenced as `REQ-{TIER}-{NNN}` (e.g. `REQ-F-001`)
- Schema types are referenced with a link to their `.json` file
- All cross-document links use relative paths
- Merged challenges: `§36 → §10`, `§39 → §3`, `§48 → §2` — do not create new content for these numbers
