# REQ-F-072: LF Line Ending Enforcement

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** Silent assumption — agents pipe output to Unix text tools (grep, awk, cut, wc) and assume LF line endings; CRLF produces `"value\r"` instead of `"value"` in string comparisons and field extractions

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: Low

---

## Description

The framework MUST normalize all stdout and stderr output to LF (`\n`) line endings regardless of the host platform. On Windows, the framework MUST explicitly open stdout and stderr in binary mode and write `\n` — not the platform default `\r\n`. JSON output, text output, error messages, and help text MUST all use LF-only line endings.

CRLF in output is invisible in terminal emulators but breaks every downstream Unix text tool an agent may pipe to. `grep "value"` will not match `"value\r"`. `cut -f1` will include the `\r` in the last field. `wc -l` counts correctly but extracted values are corrupted.

## Acceptance Criteria

- `tool list | cat -A | grep '\^M'` returns no matches on any platform
- JSON output written to a file contains no `\r` bytes
- Help text (`--help`) contains no `\r` bytes
- Error messages on stderr contain no `\r` bytes
- Verified on: macOS, Linux, Windows (WSL and native)

---

## Schema

No dedicated schema type — this requirement governs output encoding

---

## Wire Format

All output streams use `\n` as the line terminator. JSON output is no exception — even though JSON spec allows `\r\n`, the framework emits `\n`-only.

---

## Example

Without this requirement (broken on Windows):
```
$ tool list | grep "active"
"active\r"   ← grep matches but extracted value includes \r
$ tool list | awk '{print $2}'
"prod\r"     ← field extraction includes \r
```

With this requirement (correct on all platforms):
```
$ tool list | grep "active"
"active"
$ tool list | awk '{print $2}'
"prod"
```

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-005](f-005-locale-invariant-serialization.md) | F | Extends: locale-invariant output also requires platform-invariant line endings |
| [REQ-F-006](f-006-stdout-stderr-stream-enforcement.md) | F | Extends: stream enforcement applies to line ending consistency |
| [REQ-F-016](f-016-utf-8-sanitization-before-serialization.md) | F | Composes: UTF-8 sanitization and LF enforcement both applied before output |
