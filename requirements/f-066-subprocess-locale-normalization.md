# REQ-F-066: Subprocess Locale Normalization

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§57 Locale-Dependent Error Messages](../challenges/01-critical-ecosystem-runtime-agent-specific/57-medium-locale-errors.md)

**Addresses:** Severity: Medium / Token Spend: High / Time: Low / Context: Medium

---

## Description

The framework MUST set `LC_ALL=C` (or `LC_MESSAGES=C` and `LANG=C`) in the environment of all spawned subprocesses unless the command explicitly opts out via `preserve_locale: true`. This ensures that error messages from subprocesses (git, curl, system tools) are always in English and can be reliably pattern-matched. The framework MUST also normalize number formatting (decimal separators, thousands separators) by setting `LC_NUMERIC=C` in subprocess environments, preventing locale-dependent numeric output from breaking JSON parsing. The locale override applies only to spawned subprocesses; the framework itself always serializes using invariant locale (covered by REQ-F-005).

## Acceptance Criteria

- `git` error messages are in English regardless of the system locale.
- A subprocess that would normally emit `1.234,56` in a German locale emits `1234.56` under framework management.
- A command with `preserve_locale: true` does not have `LC_ALL=C` injected for its subprocesses.
- The parent process locale is unaffected; only subprocess environments are modified.
