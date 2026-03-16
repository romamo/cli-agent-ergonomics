# REQ-F-052: Response Size Hard Cap with Truncation Indicator

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§43 Tool Output Result Size Unboundedness](../challenges/01-critical-ecosystem-runtime-agent-specific/43-critical-output-size-unboundedness.md)

**Addresses:** Severity: Critical / Token Spend: Critical / Time: High / Context: Critical

---

## Description

The framework MUST enforce a maximum output size for all command responses. The default cap MUST be 1 MB (1,048,576 bytes) for JSON output and configurable via `TOOL_MAX_OUTPUT_BYTES` environment variable. When a response exceeds the cap, the framework MUST truncate the `data` array or string value, set `meta.truncated = true`, populate `meta.total_count` (total available items), `meta.returned_count` (items actually returned), and include a `meta.truncation_hint` field with the exact flag to pass (e.g., `--limit N --cursor <token>`) to retrieve the remaining data. The framework MUST NOT silently omit data without these indicators.

## Acceptance Criteria

- A command that returns 10,000 items is automatically truncated at the cap with `meta.truncated: true`.
- `meta.truncation_hint` contains a valid command invocation to retrieve the next page.
- A response under the cap does not include `meta.truncated` or includes it as `false`.
- Setting `TOOL_MAX_OUTPUT_BYTES=5242880` raises the cap to 5 MB for all commands.
