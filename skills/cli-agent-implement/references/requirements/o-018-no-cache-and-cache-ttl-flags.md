# REQ-O-018: --no-cache and --cache-ttl Flags

**Tier:** Opt-In | **Priority:** P3

**Source:** [§30 Undeclared Filesystem Side Effects](../challenges/05-high-environment-and-state/30-medium-filesystem-side-effects.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Low

---

## Description

For commands that write to caches, the framework MUST provide `--no-cache` (skip cache reads and writes for this invocation) and `--cache-ttl <seconds>` (override the default cache TTL). These flags MUST be automatically available on commands that declare a `cache` entry in `filesystem_side_effects` (REQ-C-011). With `--no-cache`, the command MUST NOT read from or write to any declared cache path.

## Acceptance Criteria

- `--no-cache` causes the command to bypass all declared cache files.
- `--cache-ttl 0` is equivalent to `--no-cache`.
- Cache files older than `--cache-ttl` seconds are treated as missing (re-fetched).
- The flags are absent on commands that declare no cache side effects.
