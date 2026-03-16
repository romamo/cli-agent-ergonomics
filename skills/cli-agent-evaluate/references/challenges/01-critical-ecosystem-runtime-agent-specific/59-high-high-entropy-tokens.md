> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §59

## 59. High-Entropy String Token Poisoning

**Source:** Gemini `02_output_context.md` (RA)

**Severity:** High | **Frequency:** Common | **Detectability:** Medium | **Token Spend:** High | **Time:** Low | **Context:** High

### The Problem

JWTs, API keys, UUIDs, base64 blobs, and cryptographic hashes in tool output consume hundreds of LLM tokens each — yet provide zero useful signal to the agent. A single `Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` in a debug dump wastes 200–400 tokens on an opaque string the agent cannot interpret. Over a session with dozens of tool calls, high-entropy fields silently consume a significant fraction of the context budget.

```bash
$ tool auth token --show
{
  "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEyMyIsImlhdCI6MTcxMDAwMDAwMCwiZXhwIjoxNzEwMDAzNjAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "expires_at": "2024-03-11T15:00:00Z"
}
# The JWT consumes ~300 tokens. The agent only needed "expires_at".
```

Worse: the same high-entropy strings appear across multiple tool responses (resource IDs, session tokens, correlation IDs), each adding wasteful repetition to the context window.

### Impact

- Context budget eroded silently by opaque strings the agent cannot reason about
- Long tokens increase per-call API cost directly
- Repeated high-entropy fields across multiple calls fill context with noise
- Agents may attempt to reason about or pattern-match JWT segments, wasting reasoning tokens

### Solutions

**Auto-mask high-entropy fields in structured output:**
```json
{
  "token": "[JWT: expires 2024-03-11T15:00:00Z, sub=user_123]",
  "token_raw": "<available via: tool auth token --show --unmask>"
}
```

**Schema marks fields as `high_entropy: true`:**
```json
{ "name": "token", "type": "string", "high_entropy": true, "mask_in_output": true }
```

**Framework detects high-entropy strings automatically:**
- Strings matching `^[A-Za-z0-9+/]{40,}={0,2}$` (base64) or JWT pattern (`xxx.yyy.zzz`) are masked unless `--unmask` is passed.
- Instead of the raw value, output: entropy type, meaningful metadata extracted from the payload (expiry, subject), and the flag to retrieve the raw value.

**For framework design:**
- Framework MUST provide a `high_entropy` field type with automatic masking in non-`--unmask` mode.
- The mask replacement MUST include the semantic metadata from the string (JWT: expiry + claims summary; UUID: just the ID truncated; API key: first 8 chars + `...`).
- `--unmask` flag explicitly opts into showing raw high-entropy values.
