# REQ-O-022: --secret-from-env / --secret-from-file Flags

**Tier:** Opt-In | **Priority:** P1

**Source:** [§24 Authentication & Secret Handling](../challenges/03-critical-security/24-critical-auth-secrets.md)

**Addresses:** Severity: Critical / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST provide `--<name>-from-env <VAR_NAME>` and `--<name>-from-file <PATH>` flag patterns for any command parameter declared as a secret. The framework reads the secret value from the environment variable or file at execution time and passes it to the command without the value ever appearing in the process argument list. The framework MUST validate that the env var or file exists before execution (exit `2` if not found).

## Acceptance Criteria

- `--token-from-env MY_TOKEN` reads the token from `$MY_TOKEN` without exposing it in `ps aux`.
- `--token-from-file /run/secrets/token` reads the token from the file.
- A missing env var or file causes exit `2` with a validation error before any side effects.
- The secret value never appears in the audit log (REQ-F-034 redaction applies).
