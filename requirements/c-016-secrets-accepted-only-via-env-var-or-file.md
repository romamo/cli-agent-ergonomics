# REQ-C-016: Secrets Accepted Only via Env Var or File

**Tier:** Command Contract | **Priority:** P1

**Source:** [§24 Authentication & Secret Handling](../challenges/03-critical-security/24-critical-auth-secrets.md)

**Addresses:** Severity: Critical / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

Commands MUST NOT declare parameters intended to receive secret values (tokens, passwords, keys) as positional or named command-line arguments. Secrets MUST be accepted via environment variable references only. The framework MUST provide `--secret-from-env VAR_NAME` and `--secret-from-file PATH` as standard flag templates that command authors use instead of bare `--password` style flags. The framework MUST reject command registrations that declare a parameter matching the secret field pattern (REQ-F-034) as a direct CLI argument.

## Acceptance Criteria

- No framework-based command accepts `--password`, `--token`, or `--api-key` as a direct argument containing the secret value.
- Commands that need a secret declare it via `--token-from-env` or `--token-from-file` pattern.
- The framework raises a registration error if a command declares a secret-named argument as a direct value argument.
- Environment variable names used for secrets are documented in the command's `--schema` output.
