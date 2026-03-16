# REQ-O-004: --output jsonl / --stream Flag

**Tier:** Opt-In | **Priority:** P2

**Source:** [§5 Pagination & Large Output](../challenges/04-critical-output-and-parsing/05-high-pagination.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Critical

---

## Description

For commands that process or return large datasets, the framework MUST support `--stream` (equivalent to `--output jsonl`) which emits one JSON object per line as results are produced, rather than buffering all results before emitting. Commands that support streaming MUST declare `supports_streaming: true`. In streaming mode, pagination metadata MUST be emitted as a final summary line.

## Acceptance Criteria

- `--stream` causes output to begin appearing before the command completes.
- Each line of streaming output is a valid, self-contained JSON object.
- The final line of streaming output is a summary object containing `pagination` metadata.
- A command that does not declare `supports_streaming: true` emits a warning when `--stream` is passed.
