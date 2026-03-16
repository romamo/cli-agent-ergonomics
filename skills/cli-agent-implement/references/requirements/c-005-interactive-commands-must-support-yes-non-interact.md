# REQ-C-005: Interactive Commands Must Support --yes / --non-interactive

**Tier:** Command Contract | **Priority:** P0

**Source:** [§10 Interactivity & TTY Requirements](../challenges/02-critical-execution-and-reliability/10-critical-interactivity.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

Any command that would prompt the user for confirmation or input in interactive mode MUST accept `--yes` (auto-confirm all prompts) and `--non-interactive` (fail immediately with exit code 4 if any prompt would be shown). The framework MUST register these flags automatically for any command that declares it uses interactive prompts. Command authors MUST declare prompt usage in registration metadata.

## Acceptance Criteria

- A command that prompts for confirmation in interactive mode accepts `--yes` and proceeds without prompting.
- With `--non-interactive`, a command that would prompt exits with exit code 4 and a JSON error.
- The `--yes` flag is idempotent: passing it to a command that never prompts has no effect.
- The `--schema` output for interactive commands includes `interactive: true`.
