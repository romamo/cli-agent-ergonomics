# REQ-F-035: External Data Trust Tagging

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§25 Prompt Injection via Output](../challenges/03-critical-security/25-critical-prompt-injection.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: High

---

## Description

When a command returns data that originated from an external, untrusted source (files, API responses, database records), the framework MUST tag that data with `"_source": "external"` and `"_trusted": false` at the top level of the `data` object. The framework MUST provide a command author API to mark specific fields or the entire `data` object as external. Commands that return purely internal computed results MAY omit these tags.

## Acceptance Criteria

- A command that reads and returns file contents includes `"_trusted": false` in its `data` object.
- A command that returns an API response includes `"_source": "external"` in its `data` object.
- A command that returns a self-computed status (no external data) may omit trust tags.
- Passing `--no-injection-protection` (REQ-O-023) suppresses trust tagging.
