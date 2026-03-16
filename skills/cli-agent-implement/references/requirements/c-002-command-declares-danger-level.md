# REQ-C-002: Command Declares Danger Level

**Tier:** Command Contract | **Priority:** P0

**Source:** [§23 Side Effects & Destructive Operations](../challenges/03-critical-security/23-critical-destructive-ops.md)

**Addresses:** Severity: Critical / Token Spend: Medium / Time: High / Context: Medium

---

## Description

Every command MUST declare a `danger_level` as part of its registration metadata, chosen from: `safe` (read-only, no side effects), `mutating` (creates or modifies state), or `destructive` (permanently deletes or irreversibly modifies state). The framework MUST refuse to register a command without this declaration. The framework MUST use this declaration to enforce related behaviors (e.g., requiring `--dry-run` for destructive commands per REQ-C-004).

## Acceptance Criteria

- Attempting to register a command without `danger_level` raises a framework error.
- The `--schema` output for every command includes `danger_level`.
- Commands with `danger_level: "destructive"` trigger framework-level dry-run enforcement (REQ-C-004).
- Commands with `danger_level: "safe"` do not require `--idempotency-key` (REQ-C-007).
