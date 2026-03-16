# REQ-F-021: Data/Meta Separation in Response Envelope

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§7 Output Non-Determinism](../challenges/04-critical-output-and-parsing/07-medium-output-nondeterminism.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST place all volatile fields (timestamps, durations, request IDs, tool version, config hash) into the `meta` object of the response envelope, and MUST keep the `data` object free of volatile fields. The framework MUST document that `data` is safe for caching and change-detection, and that `meta` is not. Commands MUST NOT place timestamps or random values directly in `data`; the framework MUST enforce this via the schema declaration mechanism.

## Acceptance Criteria

- Two responses for the same operation with the same arguments have byte-identical `data` objects (absent business-state changes).
- All `meta` fields are volatile by definition and are excluded from diff-based change detection.
- A command that attempts to put a timestamp directly in `data` triggers a framework validation warning at registration time.
