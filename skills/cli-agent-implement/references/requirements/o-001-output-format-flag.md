# REQ-O-001: --output Format Flag

**Tier:** Opt-In | **Priority:** P0

**Source:** [§2 Output Format & Parseability](../challenges/04-critical-output-and-parsing/02-critical-output-format.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Medium / Context: High

---

## Description

The framework MUST register `--output <format>` as a standard flag on all commands. Supported formats MUST include at minimum: `json` (default in non-TTY), `jsonl` (one JSON object per line), `tsv` (tab-separated, for piping), and `plain` (minimal human-readable, no decoration). In `json` mode, color and prose are always suppressed. The selected format MUST be consistent across all commands in the framework.

## Acceptance Criteria

- `--output json` produces valid JSON on stdout.
- `--output jsonl` produces one valid JSON object per line.
- `--output tsv` produces tab-separated values with a header row.
- The `--output` flag is available on every command without per-command implementation.

---

## Schema

**Type:** [`response-envelope.md`](../schemas/response-envelope.md)

The `--output json` format uses the `ResponseEnvelope` shape. The `--output jsonl` and `--output tsv` formats use command-specific row shapes without the envelope wrapper.

---

## Wire Format

```bash
$ tool deploy --target staging --output json
```

```json
{
  "ok": true,
  "data": { "id": "deploy-42", "status": "complete", "target": "staging" },
  "error": null,
  "warnings": [],
  "meta": { "duration_ms": 340 }
}
```

JSONL format (one object per line, no envelope wrapper):

```bash
$ tool list --output jsonl
```

```
{"id": "1", "name": "alice"}
{"id": "2", "name": "bob"}
```

---

## Example

The framework registers `--output` globally. Command authors do not implement it per command.

```
app = Framework("tool")
app.enable_output_flag(formats=["json", "jsonl", "tsv", "plain"])

# All commands automatically accept --output json / --output jsonl / etc.
# tool deploy --target staging --output json  →  ResponseEnvelope JSON
# tool list --output tsv  →  tab-separated rows with header
```

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-003](f-003-json-output-mode-auto-activation.md) | F | Extends: `--output json` makes auto-activation explicit and overridable |
| [REQ-F-004](f-004-consistent-json-response-envelope.md) | F | Provides: `ResponseEnvelope` used by `--output json` mode |
| [REQ-O-002](o-002-fields-selector.md) | O | Composes: `--fields` filters the `data` object within `--output json` responses |
| [REQ-O-004](o-004-output-jsonl-stream-flag.md) | O | Specializes: `--output jsonl` is the non-buffered streaming variant |
