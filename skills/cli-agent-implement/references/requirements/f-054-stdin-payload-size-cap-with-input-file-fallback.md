# REQ-F-054: Stdin Payload Size Cap with --input-file Fallback

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§61 Bidirectional Pipe Payload Deadlock](../challenges/01-critical-ecosystem-runtime-agent-specific/61-critical-pipe-payload-deadlock.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST enforce a maximum stdin read size (default: 65536 bytes, configurable via `TOOL_MAX_STDIN_BYTES`). If a stdin read would exceed this limit, the framework MUST exit with code 2 and a structured error directing the caller to use `--input-file <path>` instead. The `--input-file` flag MUST be automatically registered by the framework for any command that declares stdin input. This prevents bidirectional pipe deadlocks caused by the UNIX kernel pipe buffer limit.

## Acceptance Criteria

- A stdin payload of 65537 bytes exits with code 2 and `error.code: "STDIN_TOO_LARGE"`.
- The error includes `hint` pointing to `--input-file`.
- A command that declares `stdin_input: true` automatically has `--input-file` registered as a flag.
- A payload of 65535 bytes is accepted and processed normally.
