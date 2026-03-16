# REQ-O-023: --no-injection-protection Flag

**Tier:** Opt-In | **Priority:** P3

**Source:** [§25 Prompt Injection via Output](../challenges/03-critical-security/25-critical-prompt-injection.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: High

---

## Description

The framework's external data trust tagging (REQ-F-035) MAY be bypassed for a specific invocation by passing `--no-injection-protection`. This escape hatch is intended for trusted sources (e.g., reading internal configuration authored by the operator). When this flag is passed, external data is not wrapped with trust markers. The flag MUST be logged in the audit trail. The flag MUST require explicit acknowledgment in non-interactive mode.

## Acceptance Criteria

- `--no-injection-protection` causes external data to be returned without `_trusted: false` tagging.
- Use of this flag is recorded in the audit log with a warning.
- The flag is documented with a security warning in `--help` output.
