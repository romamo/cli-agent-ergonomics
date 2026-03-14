# REQ-F-020: Stable Array Sorting in JSON Output

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§7 Output Non-Determinism](../challenges/04-critical-output-and-parsing/07-medium-output-nondeterminism.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

In JSON output mode, the framework MUST sort all array fields in a stable, deterministic order before serialization. Arrays of objects MUST be sorted by a stable primary key (declared by the command author). Arrays of strings MUST be sorted lexicographically. Arrays of numbers MUST be sorted numerically ascending. The sort MUST be consistent across runs with identical inputs.

## Acceptance Criteria

- Two invocations of the same command with the same arguments produce byte-identical JSON output (excluding `meta` volatile fields).
- A string array output field is always in lexicographic order.
- An object array output field is always sorted by the declared primary key.
