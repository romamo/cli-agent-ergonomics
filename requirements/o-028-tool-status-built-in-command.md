# REQ-O-028: tool status Built-In Command

**Tier:** Opt-In | **Priority:** P2

**Source:** [§26 Stateful Commands & Session Management](../challenges/05-high-environment-and-state/26-high-session-management.md) · [§30 Undeclared Filesystem Side Effects](../challenges/05-high-environment-and-state/30-medium-filesystem-side-effects.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST provide a built-in `tool status` command with subflags `--show-config` (alias for REQ-O-015), `--show-side-effects` (inventory of all filesystem side effect paths with sizes), and `--show-state-files` (list of all global state files with their current values). Each flag produces a structured JSON output. The command MUST be safe (no side effects, `danger_level: "safe"`).

## Acceptance Criteria

- `tool status --show-side-effects --output json` returns paths, types, and sizes for all declared side effects.
- `tool status --show-state-files --output json` returns paths and summaries of all global state files (e.g., current context, cached tokens).
- The command exits `0` and produces valid JSON regardless of what state exists.
- All path values in the output are absolute.
