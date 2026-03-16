# REQ-C-008: Multi-Step Commands Emit Step Manifest

**Tier:** Command Contract | **Priority:** P1

**Source:** [§13 Partial Failure & Atomicity](../challenges/02-critical-execution-and-reliability/13-critical-partial-failure.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Medium

---

## Description

Any command whose execution consists of multiple discrete, ordered steps MUST declare a step manifest in its registration metadata. The manifest MUST list step names in execution order. When running with `--output json` or in streaming mode, the command MUST emit a step-start and step-complete event for each step as it executes (via the framework's step tracking API). The final response MUST include `completed_steps`, `failed_step` (if any), and `skipped_steps`.

## Acceptance Criteria

- A multi-step command's schema output includes `steps: [...]` listing all step names.
- A partial failure response includes `completed_steps` as an array of completed step names.
- A partial failure response includes `failed_step` as the name of the failed step.
- The SIGTERM/timeout response includes the same step tracking fields.
