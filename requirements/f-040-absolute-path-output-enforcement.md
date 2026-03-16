# REQ-F-040: Absolute Path Output Enforcement

**Tier:** Framework-Automatic | **Priority:** P2

**Source:** [§29 Working Directory Sensitivity](../challenges/05-high-environment-and-state/29-medium-working-directory.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: Low

---

## Description

The framework MUST provide a path output type that commands declare for any field containing a filesystem path. When a command outputs a path using this type, the framework MUST automatically resolve it to an absolute path before serialization. The framework MUST document this behavior so command authors know to use the path type rather than raw strings for paths.

## Acceptance Criteria

- A command that returns `"./src/index.ts"` as a path field has it resolved to `"/project/src/index.ts"` in the output.
- The resolved path is absolute regardless of the CWD from which the command was invoked.
- A relative path returned through the path type is always expanded against the effective CWD at invocation time.
