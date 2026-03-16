# REQ-F-058: High-Entropy Field Masking

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§59 High-Entropy String Token Poisoning](../challenges/01-critical-ecosystem-runtime-agent-specific/59-high-high-entropy-tokens.md)

**Addresses:** Severity: High / Token Spend: High / Time: Low / Context: High

---

## Description

The framework MUST automatically detect and mask high-entropy string values in JSON output unless `--unmask` is explicitly passed. Detection criteria: strings matching base64 pattern (`[A-Za-z0-9+/]{40,}={0,2}`), JWT three-part structure (`[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`), or fields declared `high_entropy: true` in the command schema. Masked values MUST be replaced with a semantic summary: for JWTs — `[JWT: sub=<sub>, exp=<exp>]`; for API keys — `[KEY: <first8>...]`; for base64 — `[BASE64: <bytecount> bytes]`. The raw value MUST be accessible via `--unmask`.

## Acceptance Criteria

- A JWT in a response field is replaced with `[JWT: sub=user_123, exp=2024-03-11T15:00:00Z]` by default.
- A 256-character base64 string is replaced with `[BASE64: 192 bytes]` by default.
- `--unmask` produces the raw value.
- Fields declared `high_entropy: true` in the schema are always masked regardless of content pattern.
