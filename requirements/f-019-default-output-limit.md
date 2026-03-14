# REQ-F-019: Default Output Limit

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§5 Pagination & Large Output](../challenges/04-critical-output-and-parsing/05-high-pagination.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Critical

---

## Description

The framework MUST apply a default result limit of 20 items to every list command. This limit MUST be overridable by the caller using `--limit <n>`, and MUST be configurable per command by the author. An explicit `--limit 0` MUST disable the limit entirely (no implicit cap). The default limit MUST be documented in the command's schema output.

## Acceptance Criteria

- A list command invoked with no flags returns at most 20 items.
- `--limit 100` returns at most 100 items.
- `--limit 0` returns all available items.
- The default limit is visible in `tool <cmd> --schema`.
