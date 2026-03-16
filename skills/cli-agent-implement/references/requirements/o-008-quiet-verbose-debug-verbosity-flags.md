# REQ-O-008: --quiet / --verbose / --debug Verbosity Flags

**Tier:** Opt-In | **Priority:** P1

**Source:** [§4 Verbosity & Token Cost](../challenges/04-critical-output-and-parsing/04-medium-verbosity.md)

**Addresses:** Severity: Medium / Token Spend: High / Time: Low / Context: High

---

## Description

The framework MUST provide `--quiet` (suppress all stderr; stdout JSON only), `--verbose` (progress messages on stderr), and `--debug` (full debug trace on stderr) as standard flags on every command. These MUST override the auto-quiet behavior (REQ-F-038). The verbosity levels MUST be mutually exclusive. In `--debug` mode, all framework-internal operations (config loading, lock acquisition, HTTP requests) MUST be logged to stderr.

## Acceptance Criteria

- `--quiet` produces zero bytes on stderr (even for warnings).
- `--verbose` produces progress messages on stderr and the JSON result on stdout.
- `--debug` produces full diagnostic trace on stderr including all HTTP requests and config resolution steps.
- Passing `--verbose` with `CI=true` overrides the auto-quiet mode.
