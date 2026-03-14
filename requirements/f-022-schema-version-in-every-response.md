# REQ-F-022: Schema Version in Every Response

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§22 Schema Versioning & Output Stability](../challenges/06-high-errors-and-discoverability/22-high-schema-versioning.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST automatically inject `meta.schema_version` (semver string) into every response. The schema version MUST correspond to the version of the response contract for that command, not the overall tool version. Callers MUST be able to detect schema changes by comparing `meta.schema_version` values across responses.

## Acceptance Criteria

- Every response JSON object includes `meta.schema_version` as a semver string.
- When a command's output schema changes in a breaking way, `meta.schema_version` increments the major version component.
- `meta.schema_version` is stable across invocations of the same command version.
