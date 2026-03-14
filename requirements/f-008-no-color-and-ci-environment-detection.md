# REQ-F-008: NO_COLOR and CI Environment Detection

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§8 ANSI & Color Code Leakage](../challenges/04-critical-output-and-parsing/08-high-ansi-leakage.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: Medium

---

## Description

The framework MUST check for `NO_COLOR` (any value, including empty, per no-color.org), `CI`, `GITHUB_ACTIONS`, `JENKINS_URL`, and `TERM=dumb` at startup. When any of these is present, the framework MUST disable all color and formatting output globally, including for stderr. The framework MUST also set `NO_COLOR=1` in the process environment so that child processes and third-party libraries inherit the setting.

## Acceptance Criteria

- When `NO_COLOR=` (empty string), all ANSI output is disabled.
- A child process spawned by the framework inherits `NO_COLOR=1`.
- `TERM=dumb` alone is sufficient to disable all color output.
