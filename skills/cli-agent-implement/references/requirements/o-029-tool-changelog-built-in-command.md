# REQ-O-029: tool changelog Built-In Command

**Tier:** Opt-In | **Priority:** P2

**Source:** [§22 Schema Versioning & Output Stability](../challenges/06-high-errors-and-discoverability/22-high-schema-versioning.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST provide a built-in `tool changelog` command that outputs a structured history of schema changes. The output MUST include: version, release date, list of added fields, list of removed fields, list of changed field types, and whether each version is a breaking change. The command MUST accept `--since <version>` to filter. This enables callers to determine what changed since the version they were built against.

## Acceptance Criteria

- `tool changelog --output json` returns a valid JSON array of version entries.
- Each entry includes `version`, `date`, `breaking` (boolean), `added`, `removed`, `changed`.
- `--since 1.0.0` returns only entries for versions after `1.0.0`.
- Breaking changes are correctly flagged as `"breaking": true`.
