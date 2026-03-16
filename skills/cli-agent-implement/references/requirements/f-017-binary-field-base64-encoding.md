# REQ-F-017: Binary Field Base64 Encoding

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§9 Binary & Encoding Safety](../challenges/04-critical-output-and-parsing/09-high-binary-encoding.md)

**Addresses:** Severity: High / Token Spend: Low / Time: Medium / Context: Low

---

## Description

When a command returns a value that cannot be represented as valid UTF-8 text, the framework MUST automatically encode it as a structured object: `{"type": "binary", "encoding": "base64", "value": "<base64 string>", "size_bytes": <integer>}`. Command authors MUST be able to declare a field as potentially binary; the framework handles encoding transparently. The framework MUST also accept a `content_type` annotation that is passed through as `"content_type"` in the wrapper object.

## Acceptance Criteria

- A command that returns raw PNG bytes produces valid JSON with a `base64`-encoded value wrapper.
- The `size_bytes` field in the wrapper matches the original byte length.
- A consuming caller can recover the original bytes by base64-decoding `value`.
