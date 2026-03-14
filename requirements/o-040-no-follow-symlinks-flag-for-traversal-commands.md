# REQ-O-040: --no-follow-symlinks Flag for Traversal Commands

**Tier:** Opt-In | **Priority:** P1

**Source:** [§66 Symlink Loop and Recursive Traversal Exhaustion](../challenges/01-critical-ecosystem-runtime-agent-specific/66-high-symlink-loop.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Critical / Context: Low

---

## Description

The framework MUST auto-register `--no-follow-symlinks` and `--max-depth <n>` (default: 50) for all commands declared with `recursive_traversal: true`. When `--no-follow-symlinks` is passed, the framework's traversal utility skips all symlinks, preventing loop detection from being needed. When `--max-depth` is exceeded, the command exits with code 4 and a structured error listing the depth limit and suggesting `--max-depth` adjustment.

## Acceptance Criteria

- `tool delete --recursive --no-follow-symlinks /tmp/a` skips symlinks and completes without following circular references.
- `tool delete --recursive --max-depth 3 /deep/tree` exits 4 with `DEPTH_EXCEEDED` if the tree is deeper than 3 levels.
- Without `--no-follow-symlinks`, the inode tracking from REQ-F-061 provides the loop protection.
- `--schema` for recursive commands lists `no-follow-symlinks` and `max-depth` flags.
