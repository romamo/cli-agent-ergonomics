# REQ-C-011: Commands Declare Filesystem Side Effects

**Tier:** Command Contract | **Priority:** P3

**Source:** [§30 Undeclared Filesystem Side Effects](../challenges/05-high-environment-and-state/30-medium-filesystem-side-effects.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Low

---

## Description

Command authors MUST declare all filesystem side effects in the command's registration metadata using the `filesystem_side_effects` array. Each entry MUST specify: `path` (template or glob), `type` (one of: `cache`, `log`, `temp`, `credential`, `config`), `ttl_seconds` (if applicable), and `clearable_with` (the framework command to clear it). The framework uses this information for `tool status --show-side-effects` and `tool cleanup`.

## Acceptance Criteria

- A command that writes to a cache directory declares that path in `filesystem_side_effects`.
- `tool status --show-side-effects` lists all paths declared by registered commands.
- `tool cleanup` removes all paths declared as `type: "temp"` or `type: "cache"`.
