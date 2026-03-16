# REQ-F-001: Standard Exit Code Table

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§1 Exit Codes & Status Signaling](../challenges/04-critical-output-and-parsing/01-critical-exit-codes.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: High / Context: Low

---

## Description

The framework MUST define and enforce a fixed, documented exit code table. Commands MUST NOT exit with any code outside this table for a standard condition. The table MUST include: `0` (success), `1` (general error — last resort), `2` (operation started but failed mid-way, partial side effects), `3` (argument/validation error — zero side effects guaranteed), `4` (precondition not met), `5` (not found), `6` (conflict / already exists), `7` (permission denied — valid credentials, wrong access level), `8` (auth required — credentials missing or invalid), `9` (payment required), `10` (timeout — partial side effects possible), `11` (rate limited — retry after back-off), `12` (service unavailable), `13` (command redirected — use replacement verbatim). The framework MUST provide named constants for every code; commands MUST reference these constants, never literal integers.

## Acceptance Criteria

- Every exit code emitted by a framework-based command appears in the framework's code table
- Named constants (e.g., `ExitCode.NOT_FOUND`) exist for every table entry
- The framework rejects command registrations that attempt to exit with an undeclared code
- `exit 0` is emitted if and only if the operation completed as intended
- `exit 1` is never emitted for conditions that have a more specific code

---

## Schema

**Types:** [`exit-code.md`](../schemas/exit-code.md)

| Code | Constant | Retryable | Side effects at exit |
|------|----------|-----------|----------------------|
| 0 | `SUCCESS` | — | complete |
| 1 | `GENERAL_ERROR` | depends | unknown |
| 2 | `PARTIAL_FAILURE` | no | partial |
| 3 | `ARG_ERROR` | yes | **none** (REQ-F-002) |
| 4 | `PRECONDITION` | depends | none |
| 5 | `NOT_FOUND` | no | none |
| 6 | `CONFLICT` | no | none |
| 7 | `PERMISSION_DENIED` | no | none |
| 8 | `AUTH_REQUIRED` | yes* | none |
| 9 | `PAYMENT_REQUIRED` | yes* | none |
| 10 | `TIMEOUT` | yes | partial |
| 11 | `RATE_LIMITED` | yes | none |
| 12 | `UNAVAILABLE` | yes | none |
| 13 | `REDIRECTED` | yes | none |

\* Retryable only after the prerequisite condition is resolved.

Reserved ranges: `14–63` framework extensions · `64–78` POSIX sysexits compatibility (optional mapping) · `79–125` command-specific (declare via REQ-C-001) · `126–255` shell-reserved, MUST NOT use.

---

## Example

Framework-Automatic: no command author action needed. The framework registers the table at startup and provides named constants for import.

```
# Correct — named constant
raise CommandError(ExitCode.NOT_FOUND, "User not found")

# Rejected at registration — literals not permitted
raise CommandError(5, "User not found")
→ FrameworkError: use ExitCode.NOT_FOUND, not literal 5
```

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-002](f-002-exit-code-2-reserved-for-validation-failures.md) | F | Specializes: enforces reserved semantics for `ARG_ERROR (3)` — zero side effects guarantee |
| [REQ-C-001](c-001-command-declares-exit-codes.md) | C | Consumes: commands declare which `ExitCode` values they may emit |
| [REQ-C-013](c-013-error-responses-include-code-and-message.md) | C | Composes: JSON error responses carry an `ExitCode` value in `error.code` |
| [REQ-F-004](f-004-consistent-json-response-envelope.md) | F | Composes: envelope `ok` is derived from whether exit code is `SUCCESS` |
| [REQ-O-041](o-041-tool-manifest-built-in-command.md) | O | Exposes: manifest includes the exit code table per command |
