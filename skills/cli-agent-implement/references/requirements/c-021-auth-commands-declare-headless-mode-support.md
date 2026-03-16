# REQ-C-021: Auth Commands Declare Headless Mode Support

**Tier:** Command Contract | **Priority:** P0

**Source:** [§45 Headless Authentication / OAuth Browser Flow Blocking](../challenges/01-critical-ecosystem-runtime-agent-specific/45-critical-headless-auth.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

Any command that performs authentication or credential acquisition MUST declare `headless_supported: true | false` in its registration metadata. Commands with `headless_supported: false` MUST also declare `token_env_vars: [...]` — the list of environment variable names that can supply a pre-acquired token instead. When a `headless_supported: false` command is invoked in non-TTY mode without a populated token env var, the framework MUST exit with code 4 and a structured error listing the required env vars. Command authors MUST NOT launch browser redirects in non-TTY mode.

## Acceptance Criteria

- A browser-auth command invoked in non-TTY mode without a token env var exits with code 4 and lists the required env vars.
- A browser-auth command invoked in non-TTY mode with a valid token in `MY_TOOL_TOKEN` succeeds.
- The `--schema` output for auth commands includes `headless_supported` and `token_env_vars`.
- A headless-supported auth command (e.g., device code flow) works in non-TTY mode without any token env var.
