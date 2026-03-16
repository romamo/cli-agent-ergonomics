# REQ-O-027: tool cleanup Built-In Command

**Tier:** Opt-In | **Priority:** P2

**Source:** [§30 Undeclared Filesystem Side Effects](../challenges/05-high-environment-and-state/30-medium-filesystem-side-effects.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Low

---

## Description

The framework MUST provide a built-in `tool cleanup` command that removes all known filesystem side effect paths declared by registered commands. The command MUST accept `--scope <type>` (one of: `all`, `temp`, `cache`, `logs`) to limit cleanup to specific categories. The command MUST output a structured JSON summary of what was removed and total disk space reclaimed. The command MUST NOT remove files younger than `--min-age <seconds>` (default: 0).

## Acceptance Criteria

- `tool cleanup --scope temp` removes all paths declared as `type: "temp"` in command schemas.
- `tool cleanup --output json` returns a list of removed paths and total bytes freed.
- `tool cleanup --min-age 3600` does not remove any file or directory created in the last hour.
- `tool cleanup --scope cache` does not affect logs or temp files.
