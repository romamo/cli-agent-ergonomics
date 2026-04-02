# REQ-F-075: Subcommand Additive Stability

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** Silent assumption — agents build internal models of a tool's command tree and reuse them across invocations; removed or renamed subcommands produce "command not found" errors with no indication that the interface changed

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: Medium

---

## Description

The framework MUST enforce that subcommands, flags, and their documented exit codes are additive across patch and minor versions — they can be added but never removed or renamed without a deprecation period. A deprecated subcommand or flag MUST remain functional and emit a structured deprecation warning on stderr for at least one minor version before removal. The deprecation warning MUST include the replacement command or flag.

The framework MUST register the tool version at which each subcommand was introduced, and optionally the version at which it was deprecated, in the manifest response. This allows agents to perform compatibility checks before constructing invocations.

## Acceptance Criteria

- Removing a subcommand without a prior deprecation release causes a framework registration error at startup
- A deprecated subcommand executes normally and emits `{"level":"warn","code":"DEPRECATED","message":"use X instead","replacement":"tool new-sub"}` to stderr
- `tool manifest` lists `introduced_in` and `deprecated_in` (if applicable) for each subcommand
- Upgrading from version N to N+1 never causes a previously working agent invocation to produce "unknown command" without prior warning

---

## Schema

`manifest-response` — subcommand entries include `introduced_in` and optionally `deprecated_in` and `replacement`

---

## Wire Format

Deprecation warning on stderr (structured):

```json
{"level": "warn", "code": "DEPRECATED", "message": "tool old-sub is deprecated since 2.0.0; use tool new-sub instead", "replacement": "tool new-sub", "removed_in": "3.0.0"}
```

Manifest entry:

```json
{
  "name": "old-sub",
  "introduced_in": "1.0.0",
  "deprecated_in": "2.0.0",
  "replacement": "new-sub",
  "removed_in": "3.0.0"
}
```

---

## Example

```
$ tool old-sub --flag value
→ stderr: {"level":"warn","code":"DEPRECATED","message":"use tool new-sub instead","replacement":"tool new-sub"}
→ stdout: (normal output — command still works)
→ exit code: 0
```

Agent receiving this deprecation warning self-migrates to `tool new-sub` on the next invocation.

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-022](f-022-schema-version-in-every-response.md) | F | Composes: schema version bumped when subcommand tree changes |
| [REQ-F-023](f-023-tool-version-in-every-response.md) | F | Provides: tool version used to gate compatibility checks |
| [REQ-O-041](o-041-tool-manifest-built-in-command.md) | O | Provides: manifest command exposing subcommand lifecycle metadata |
| [REQ-O-029](o-029-tool-changelog-built-in-command.md) | O | Provides: changelog command listing removals and replacements |
