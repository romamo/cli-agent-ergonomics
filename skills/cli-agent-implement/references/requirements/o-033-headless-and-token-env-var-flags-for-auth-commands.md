# REQ-O-033: --headless and --token-env-var Flags for Auth Commands

**Tier:** Opt-In | **Priority:** P0

**Source:** [§45 Headless Authentication / OAuth Browser Flow Blocking](../challenges/01-critical-ecosystem-runtime-agent-specific/45-critical-headless-auth.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

Any command that performs authentication MUST support `--headless` and `--token-env-var <VAR_NAME>` flags (automatically registered by the framework for commands with `auth: true` in their metadata). When `--headless` is passed, the command MUST skip any browser redirect and instead check the environment variable named by `--token-env-var` (or the default token env vars declared in REQ-C-021). If `--headless` is active and no token is found, the command MUST exit with code 4 and a structured error listing the expected env var name and how to populate it. When stdin is not a TTY, `--headless` behavior MUST be the default.

## Acceptance Criteria

- `command login --headless --token-env-var MY_TOKEN` reads `MY_TOKEN` from environment without opening a browser.
- `command login --headless` without a token exits with code 4, listing the expected env var.
- In non-TTY mode, browser auth is suppressed automatically (equivalent to `--headless`).
- `--token-env-var` accepts any valid env var name; the framework reads that variable's value as the token.
