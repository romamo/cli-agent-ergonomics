# REQ-O-026: tool doctor Built-In Command

**Tier:** Opt-In | **Priority:** P1

**Source:** [§20 Environment & Dependency Discovery](../challenges/06-high-errors-and-discoverability/20-medium-dependency-discovery.md)

**Addresses:** Severity: Medium / Token Spend: Medium / Time: Medium / Context: Low

---

## Description

The framework MUST provide a built-in `tool doctor` command that runs all registered `preflight()` hooks and reports results. Each check MUST include: `name`, `ok` (boolean), `version` found (if applicable), `required` version (if applicable), `error` message (if failed), and `fix` (exact shell command to resolve the issue). The command MUST exit `0` if all checks pass, exit `1` if any check fails. The `doctor` command MUST also test network connectivity and proxy settings for all registered network endpoints.

## Acceptance Criteria

- `tool doctor --output json` returns a structured JSON object with a `checks` array.
- Each failed check includes a `fix` field with an executable shell command.
- A missing required dependency appears as a failed check with `ok: false`.
- `tool doctor` exit code is `0` iff all checks pass.
