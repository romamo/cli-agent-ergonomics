# REQ-O-031: Dependency Version Matrix Declaration

**Tier:** Opt-In | **Priority:** P1

**Source:** [§38 Runtime Dependency Version Mismatch](../challenges/01-critical-ecosystem-runtime-agent-specific/38-high-dependency-version-mismatch.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

The framework MUST provide a mechanism for declaring all required runtime dependencies (external binaries, runtimes, and system libraries) with their minimum and maximum compatible version constraints. Each declared dependency MUST include: `name`, `check_command` (exact shell command to verify presence), `version_regex` (regex to extract the version string from check_command output), `min_version`, `max_version` (optional), and `fix_command` (exact shell command to install or upgrade). These declarations are automatically consumed by `tool doctor` (REQ-O-026) and emitted in `--schema` output.

## Acceptance Criteria

- A declared dependency with a version below `min_version` appears as a failed check in `tool doctor`.
- A declared dependency with a version above `max_version` appears as a compatibility warning in `tool doctor`.
- `tool doctor --output json` includes a `dependencies` array with all declared dependencies and their check results.
- The `fix_command` for each failed dependency is an executable shell command.
