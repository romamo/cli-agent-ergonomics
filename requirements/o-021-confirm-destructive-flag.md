# REQ-O-021: --confirm-destructive Flag

**Tier:** Opt-In | **Priority:** P0

**Source:** [§23 Side Effects & Destructive Operations](../challenges/03-critical-security/23-critical-destructive-ops.md)

**Addresses:** Severity: Critical / Token Spend: Medium / Time: High / Context: Medium

---

## Description

The framework MUST provide `--confirm-destructive` as a standard flag on all commands with `danger_level: "destructive"`. Without this flag, a destructive command MUST exit with a structured error (exit `2`) explaining that the flag is required and showing what would be affected (equivalent to an implicit `--dry-run` output). With this flag, the command proceeds. This is distinct from `--yes` (which auto-confirms interactive prompts) and specifically guards destructive operations in automated contexts.

## Acceptance Criteria

- A destructive command invoked without `--confirm-destructive` exits `2` with a JSON error listing what would be affected.
- A destructive command invoked with `--confirm-destructive` proceeds normally.
- The `--schema` output for destructive commands includes `requires_confirmation: true`.
- `--confirm-destructive` is absent on non-destructive commands.
