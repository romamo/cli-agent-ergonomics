# REQ-O-002: --fields Selector

**Tier:** Opt-In | **Priority:** P2

**Source:** [§4 Verbosity & Token Cost](../challenges/04-critical-output-and-parsing/04-medium-verbosity.md)

**Addresses:** Severity: Medium / Token Spend: High / Time: Low / Context: High

---

## Description

The framework MUST provide a `--fields <comma-separated-names>` flag on all commands. When specified, the JSON `data` object MUST contain only the listed top-level fields. Framework-level fields (`ok`, `error`, `meta`, `warnings`, `pagination`) MUST always be present regardless of `--fields`. This filtering MUST occur at the serialization layer, not requiring per-command implementation.

## Acceptance Criteria

- `--fields id,name` returns a `data` object with only `id` and `name` keys.
- `ok`, `error`, `meta` are always present even with `--fields`.
- An unknown field name in `--fields` is silently ignored (not an error).
- `--fields` is available on every command.
