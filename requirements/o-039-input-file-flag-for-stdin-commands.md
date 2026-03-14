# REQ-O-039: --input-file Flag for Stdin Commands

**Tier:** Opt-In | **Priority:** P1

**Source:** [§61 Bidirectional Pipe Payload Deadlock](../challenges/01-critical-ecosystem-runtime-agent-specific/61-critical-pipe-payload-deadlock.md) · [§50 Stdin Consumption Deadlock](../challenges/01-critical-ecosystem-runtime-agent-specific/50-critical-stdin-deadlock.md)

**Addresses:** Severity: Critical / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST automatically register `--input-file <path>` for any command that declares `stdin_input: true`. When `--input-file` is passed, the framework reads input from the file instead of stdin, bypassing the pipe buffer limit entirely. The file is read in streaming fashion; there is no size limit for file-based input. `--input-file -` is equivalent to stdin (preserving backward compatibility). The framework MUST document that payloads larger than 64KB should use `--input-file` rather than stdin piping.

## Acceptance Criteria

- `tool process --input-file /path/to/large.json` reads from the file, not stdin.
- `tool process --input-file -` reads from stdin (equivalent to piping).
- A 10MB file passed via `--input-file` is processed successfully.
- A 10MB payload via stdin is rejected with `STDIN_TOO_LARGE` and `hint: "use --input-file"`.
