---
name: cli-agent-evaluate
description: Evaluate a CLI tool against a single CLI Agent Spec challenge. Runs the challenge's check, scores 0–3, and provides an applicable agent workaround if the score is below 3. Use this for targeted single-challenge evaluation. For multi-challenge evaluation use the master evaluation skill.
license: MIT
compatibility: Requires access to the CLI being evaluated.
---

# CLI Agent Evaluate — Single Challenge

Evaluate a CLI tool against one challenge from the CLI Agent Spec spec.

## Inputs

- **Challenge** — a challenge identifier: `§N` number, a keyword (e.g. "ansi", "interactivity"), or a file path
- **CLI** — the CLI tool to evaluate: a command name (e.g. `gh`), a binary path, or enough context to run checks

---

## Local Memory Artifacts

This skill manages three local memory artifacts per CLI being evaluated. Store them locally using whatever persistence mechanism your agent supports:

| Artifact | Key | Content |
|---|---|---|
| `<cli-name>-environment` | OS, runtime, binary, version, non-interactive flags, config env vars |
| `<cli-name>-findings` | One row per completed challenge (§N, title, severity, score, date, notes) |
| `<cli-name>-issues` | Bugs and cross-challenge observations tagged by §N, discovered during evaluation |

---

## Step 0 — Load environment profile

Load `<cli-name>-environment` from local storage.

- **If it exists:** use it and proceed to Step 1.
- **If it does not exist:** run the `cli-agent-onboard` skill for this CLI first, then return to Step 1.

---

## Step 1 — Locate the challenge file

Challenge files live in `references/challenges/` relative to this skill's directory.

Find the file by matching `§N` or a keyword against the index:

```
references/challenges/index.md
```

---

## Step 2 — Read only the needed sections from the challenge file

Do not read the full file. Extract only:

1. The **metadata line** — the `**Severity:** ... | **Frequency:** ...` line immediately after the title
2. The `### Evaluation` section — score table + `**Check:**` line
3. The `### Agent Workaround` section — only if the score ends up below 3

---

## Step 3 — Run the check

The `**Check:**` line inside `### Evaluation` is self-contained. Run it against the CLI using the invocation pattern from the environment profile.

- Use the resolved binary and timeout method from the profile
- Pass `stdin=DEVNULL` (or equivalent) for any command that might prompt
- If the check requires human observation (e.g. "inspect output for X"), describe what was observed and ask the user to confirm

---

## Step 4 — Assign a score

Match the observed behavior against the score table (0–3). If the CLI falls between two levels, assign the lower score.

---

## Step 5 — Read workaround if score < 3

If score is 0, 1, or 2: read the `### Agent Workaround` section from the challenge file.
Select the techniques that apply given the gap. Substitute real values from the environment profile (actual flag names, actual binary path, actual timeout method). Omit techniques the CLI already handles.

---

## Step 6 — Emit the result

Output a structured result block:

```
## Evaluation Result

**Challenge:** §N — <title>
**Severity:** <Critical | High | Medium>
**CLI:** <tool name>
**Score:** <0–3> / 3
**Check:** <one-line summary of what was observed>

### Applicable Workaround
<workaround with real values from environment profile — omit section if score is 3>

### Notes
<bugs, unexpected behaviours, or findings relevant to other challenges — tag each with §N if known>
```

---

## Step 7 — Save findings

Load `<cli-name>-findings` if it exists. Append one row for the challenge just evaluated, then save it back. Do not rewrite rows already present.

**Format:**

```markdown
# Findings — <cli-name>

| Challenge | Title | Severity | Score | Date | Notes |
|---|---|---|---|---|---|
| §10 | Interactivity & TTY Requirements | Critical | 2/3 | 2026-03-15 | confirm() exits with error in non-TTY without --yes; pager suppressed ✓ |
```

If any bugs or unexpected behaviours were observed, load `<cli-name>-issues`, append an entry, and save it back:

```markdown
# Issues — <cli-name>

### §18 candidate — transaction add unhandled TypeError
`bean transaction add` without `--json` raises a raw stack trace instead of a clean error.
Discovered during §10 evaluation on 2026-03-15.
```

---

## Rules

- Always run Step 0 first — never skip environment discovery
- Re-use the existing profile if present; do not re-run discovery unnecessarily
- The workaround must use actual values from the environment profile, not generic placeholders
- Do not infer the score from the challenge title alone — always run the check
- If the check cannot be run automatically (no CLI access), state that explicitly and ask the user to provide the observation
- Use only the three named local artifacts (`<cli>-environment`, `<cli>-findings`, `<cli>-issues`) for persistence — do not write to any agent-specific paths
