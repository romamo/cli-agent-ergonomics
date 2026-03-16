# REQ-F-061: Symlink Loop Detection in Traversal Utilities

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§66 Symlink Loop and Recursive Traversal Exhaustion](../challenges/01-critical-ecosystem-runtime-agent-specific/66-high-symlink-loop.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Critical / Context: Low

---

## Description

The framework's filesystem traversal utilities (used by commands that copy, delete, archive, or search recursively) MUST track visited directory inodes and exit with a structured error immediately upon detecting a revisited inode (circular symlink). The framework MUST additionally enforce a maximum traversal depth (default: 50, configurable via `--max-depth`). Both checks MUST apply to the framework's built-in traversal API; commands using the framework's API get this protection automatically.

## Acceptance Criteria

- A recursive delete on a directory containing a circular symlink exits with code 4 and `error.code: "SYMLINK_LOOP"` before exhausting memory.
- The error includes `path` (where the loop was detected) and `loop_target` (the directory it points back to).
- `--max-depth 10` limits traversal to 10 directory levels.
- A directory without circular symlinks traverses normally to full depth.
