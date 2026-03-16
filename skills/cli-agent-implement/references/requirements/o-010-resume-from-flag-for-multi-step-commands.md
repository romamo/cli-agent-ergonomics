# REQ-O-010: --resume-from Flag for Multi-Step Commands

**Tier:** Opt-In | **Priority:** P2

**Source:** [§13 Partial Failure & Atomicity](../challenges/02-critical-execution-and-reliability/13-critical-partial-failure.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

Commands that implement the step manifest contract (REQ-C-008) SHOULD support `--resume-from <step-name>` to resume execution from a specific step, skipping all prior steps. Commands that support this declare `resumable: true`. The framework provides the flag parsing; commands implement the skip logic. The `resume_from` value from a partial failure response is intended to be passed directly as `--resume-from` in a retry.

## Acceptance Criteria

- `--resume-from step-3` begins execution at step 3, having skipped steps 1 and 2.
- Skipped steps appear in the response's `skipped_steps` array.
- The response `effect` correctly reflects only the work done during the resumed execution.
- Passing an invalid step name to `--resume-from` exits `2` with a validation error.
