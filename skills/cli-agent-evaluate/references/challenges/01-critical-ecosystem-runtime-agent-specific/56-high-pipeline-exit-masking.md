> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §56

## 56. Exit Code Masking in Shell Pipelines

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Low | **Context:** Low

### The Problem

When a CLI tool is used in a shell pipeline (`tool | jq '.data[]'`), the shell reports the exit code of the *last* command — `jq` — not the tool. If `tool` fails with exit 1 but outputs a valid JSON error envelope (which `jq` happily parses), `jq` exits 0. The agent sees `exit 0` and empty output, interprets this as "the command succeeded but returned no results."

```bash
# Agent runs: tool list-users | jq '.data[].id'
#
# tool exits 1 (rate limited), outputs:
# {"ok": false, "error": {"code": "RATE_LIMITED"}}
#
# jq parses this, finds no .data[].id, exits 0, outputs nothing
#
# Agent sees: exit 0, empty output → "no users exist"
# Correct interpretation: rate limited, retry after backoff

# Fix requires pipefail — but agents can't guarantee it's set:
set -o pipefail
tool list-users | jq '.data[].id'
```

### Impact

- Failed operations silently appear as successes (empty result set)
- Rate limits, auth failures, and partial errors all masked as "zero results"
- Requires `pipefail` shell option which agents cannot guarantee

### Solutions

**Primary defense: check `.ok` in the JSON envelope, not only the exit code:**
```bash
result=$(tool list-users)
echo "$result" | jq -e '.ok' > /dev/null || { echo "$result" | jq '.error'; exit 1; }
echo "$result" | jq '.data[].id'
```

**`meta.ok` mirrors top-level `ok` for pipeline detection:**
```json
{"ok": false, "meta": {"ok": false, "exit_code": 9}, "error": {...}}
```

**For framework design:**
- Document prominently: agents MUST check `.ok` in the JSON envelope, not only the exit code, when piping.
- Framework SHOULD write `TOOL_FAILED=1` to stderr on failure so pipeline callers can detect failure without `pipefail`.
