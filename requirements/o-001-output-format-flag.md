# REQ-O-001: --output Format Flag

**Tier:** Opt-In | **Priority:** P0

**Source:** [§2 Output Format & Parseability](../challenges/04-critical-output-and-parsing/02-critical-output-format.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Medium / Context: High

---

## Description

The framework MUST register `--output <format>` as a standard flag on all commands. Supported formats MUST include at minimum: `json` (default in non-TTY), `jsonl` (one JSON object per line), `tsv` (tab-separated, for piping), and `plain` (minimal human-readable, no decoration). In `json` mode, color and prose are always suppressed. The selected format MUST be consistent across all commands in the framework.

## Acceptance Criteria

- `--output json` produces valid JSON on stdout.
- `--output jsonl` produces one valid JSON object per line.
- `--output tsv` produces tab-separated values with a header row.
- The `--output` flag is available on every command without per-command implementation.
