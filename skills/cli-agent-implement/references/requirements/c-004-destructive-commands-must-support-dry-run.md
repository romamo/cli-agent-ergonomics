# REQ-C-004: Destructive Commands Must Support --dry-run

**Tier:** Command Contract | **Priority:** P0

**Source:** [§23 Side Effects & Destructive Operations](../challenges/03-critical-security/23-critical-destructive-ops.md)

**Addresses:** Severity: Critical / Token Spend: Medium / Time: High / Context: Medium

---

## Description

Every command with `danger_level: "destructive"` MUST implement a `--dry-run` mode. In dry-run mode, the command MUST perform all validation and computation but MUST NOT commit any irreversible change. The dry-run response MUST include `effect: "would_delete"` (or analogous `would_*` prefix), and MUST include a `would_affect` object describing what would be changed. The framework MUST register `--dry-run` as a standard flag for all destructive commands and MUST enforce that dry-run responses contain no actual mutations.

## Acceptance Criteria

- A destructive command with `--dry-run` never modifies any external state.
- The dry-run response includes `effect` with a `"would_"` prefix.
- The dry-run response includes a `would_affect` object with human-readable and machine-readable impact description.
- The framework raises a registration error if a destructive command does not implement `--dry-run`.
