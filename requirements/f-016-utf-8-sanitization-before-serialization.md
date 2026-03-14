# REQ-F-016: UTF-8 Sanitization Before Serialization

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§9 Binary & Encoding Safety](../challenges/04-critical-output-and-parsing/09-high-binary-encoding.md)

**Addresses:** Severity: High / Token Spend: Low / Time: Medium / Context: Low

---

## Description

The framework's JSON serializer MUST pass every string value through a UTF-8 sanitizer before serialization. The sanitizer MUST handle: non-UTF-8 byte sequences (replace with U+FFFD), null bytes (replace with U+FFFD), and lone surrogate code points. The sanitizer MUST never raise an exception or crash; it MUST always produce valid UTF-8 output.

## Acceptance Criteria

- A command that returns a Latin-1 encoded string does not crash; the output is valid UTF-8 JSON.
- A command that returns a string containing `\x00` produces valid JSON (no embedded null bytes in output).
- The framework never emits a `UnicodeDecodeError` or equivalent to stderr.
