# REQ-O-007: --stable-output Flag

**Tier:** Opt-In | **Priority:** P3

**Source:** [§7 Output Non-Determinism](../challenges/04-critical-output-and-parsing/07-medium-output-nondeterminism.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST provide a `--stable-output` flag that explicitly requests deterministic output: all arrays sorted, all volatile `meta` fields omitted from comparison, and any remaining non-deterministic content replaced with stable alternatives. Commands that declare non-deterministic fields MUST omit those fields when `--stable-output` is passed. This flag is intended for caching and change-detection use cases.

## Acceptance Criteria

- Two invocations of the same command with `--stable-output` and identical arguments produce byte-identical stdout.
- `meta.request_id` and `meta.timestamp` are omitted when `--stable-output` is passed.
- `--stable-output` implies all arrays are sorted (REQ-F-020 behavior is always-on, but this flag is a caller signal for caching intent).
