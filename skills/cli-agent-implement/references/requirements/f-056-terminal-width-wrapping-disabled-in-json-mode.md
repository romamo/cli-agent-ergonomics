# REQ-F-056: Terminal Width Wrapping Disabled in JSON Mode

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§63 Terminal Column Width Output Corruption](../challenges/01-critical-ecosystem-runtime-agent-specific/63-medium-column-width-corruption.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Low / Context: Medium

---

## Description

The framework MUST disable all terminal-width-based text wrapping when JSON output mode is active. The framework's JSON serializer MUST NOT inject newlines into string field values regardless of the value of `$COLUMNS`, `shutil.get_terminal_size()`, or `process.stdout.columns`. String values MUST be serialized as single-line JSON strings. When the `--width` flag is set to `0` (the default in non-TTY mode), all prose output on stderr is also unwrapped.

## Acceptance Criteria

- A 200-character URL in a JSON field is serialized as a single unbroken string, not split across lines.
- `$COLUMNS=40` does not cause any JSON string value to contain a newline character.
- `json.loads(stdout_output)` succeeds on all JSON mode output regardless of terminal width settings.
- In TTY mode with `--width=80`, prose output on stderr wraps at 80 characters (unchanged behavior).
