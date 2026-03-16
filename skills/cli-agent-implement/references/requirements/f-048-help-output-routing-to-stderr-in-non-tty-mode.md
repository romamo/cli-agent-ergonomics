# REQ-F-048: Help Output Routing to Stderr in Non-TTY Mode

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§3 Stderr vs Stdout Discipline](../challenges/04-critical-output-and-parsing/03-high-stderr-stdout.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: High

---

## Description

When stdout is not a TTY, the framework MUST redirect all `--help` output to stderr. In non-TTY mode, `--help` MUST additionally emit a minimal structured JSON object to stdout: `{"ok": true, "data": null, "meta": {"help": true, "schema_ref": "<command> --schema"}}`. This ensures that callers reading stdout always receive valid JSON, and agents that accidentally invoke `--help` get a machine-parseable redirect indicator rather than help text on stdout that breaks JSON parsing.

## Acceptance Criteria

- In non-TTY mode, `command --help` produces valid JSON on stdout.
- In non-TTY mode, the help text itself appears only on stderr.
- In TTY mode, `command --help` produces help text on stdout (unchanged from standard behavior).
- `json.loads(stdout_output)` succeeds on `--help` invocations in non-TTY mode.
