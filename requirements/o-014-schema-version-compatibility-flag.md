# REQ-O-014: --schema-version Compatibility Flag

**Tier:** Opt-In | **Priority:** P2

**Source:** [§22 Schema Versioning & Output Stability](../challenges/06-high-errors-and-discoverability/22-high-schema-versioning.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

Commands that have undergone breaking schema changes SHOULD support `--schema-version <major>` to request output in a prior major version format. The framework provides the flag; commands implement compatibility shims for supported historical versions. Commands MUST declare the minimum supported `--schema-version` in their registration. Callers using a pinned schema version receive a deprecation warning in `meta.warnings` when using a version below the current.

## Acceptance Criteria

- `--schema-version 1` on a v2 command produces output conforming to the v1 schema.
- A deprecation warning appears in `meta.warnings` when using an old schema version.
- Requesting a schema version below the minimum supported raises a structured error.
- The current and minimum supported schema versions are included in `--schema` output.
