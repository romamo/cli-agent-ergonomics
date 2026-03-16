# REQ-O-036: --instance-id Flag for Agent State Namespacing

**Tier:** Opt-In | **Priority:** P1

**Source:** [§58 Multi-Agent Concurrent Invocation Conflict](../challenges/01-critical-ecosystem-runtime-agent-specific/58-high-multiagent-conflict.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

The framework MUST provide `--instance-id <string>` as a global flag. When set, all per-instance state (config cache, credential cache, temp directories, lock files) is namespaced under `~/.tool/instances/<instance-id>/`. This allows multiple parallel agent instances to operate on the same machine without state conflicts. The `TOOL_INSTANCE_ID` environment variable MAY also set the instance ID. If neither is set, the framework uses a default shared namespace with file locking for all writes.

## Acceptance Criteria

- `tool --instance-id agent-1 config set region=us-east-1` writes to `~/.tool/instances/agent-1/config.json`.
- `tool --instance-id agent-2 config set region=eu-west-1` writes to a different path and does not affect agent-1's config.
- Without `--instance-id`, concurrent config writes use file locking and succeed sequentially.
- `TOOL_INSTANCE_ID=agent-3` is equivalent to `--instance-id agent-3`.
