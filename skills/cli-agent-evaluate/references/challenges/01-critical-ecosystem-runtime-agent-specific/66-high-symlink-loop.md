> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §66

## 66. Symlink Loop and Recursive Traversal Exhaustion

**Source:** Antigravity `05_environment_and_execution.md` (RA)

**Severity:** High | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Critical | **Context:** Low

### The Problem

When a CLI tool performs recursive directory traversal (copy, delete, archive, search) and encounters a circular symlink (`A → B → A`), it loops indefinitely consuming all available memory and CPU until it crashes or the system OOM-kills it. The tool emits no warning before running out of resources. Agents operating on user-provided paths cannot know in advance whether circular symlinks exist, and the tool provides no defense.

```bash
# Setup: circular symlink
$ mkdir /tmp/a && mkdir /tmp/b
$ ln -s /tmp/b /tmp/a/link_to_b
$ ln -s /tmp/a /tmp/b/link_to_a

# Agent runs a recursive delete:
$ my-tool delete --recursive /tmp/a
# Tool traverses: a/ → a/link_to_b/ → a/link_to_b/link_to_a/ → ...
# Memory grows unbounded; process hangs; eventually OOM-killed
# Agent sees: timeout, then exit (non-zero from OOM kill signal)
# No structured error; agent doesn't know if any files were deleted

# Also affects: archive commands (infinite zip), find-and-replace, hash computation
$ tool archive /tmp/a --output archive.tar.gz
# Creates a theoretically infinite archive; fills disk; crashes
```

### Impact

- Process consumes all available memory and CPU before dying
- Agent timeout fires; no information about what happened or what was deleted
- Disk may be filled by infinite archive or temp file creation
- Partial operations: some files may have been deleted/modified before the crash

### Solutions

**Track visited inodes; fail on revisit:**
```python
visited_inodes = set()
def safe_walk(path):
    inode = os.stat(path).st_ino
    if inode in visited_inodes:
        raise SymlinkLoopError(f"Circular symlink detected at {path}")
    visited_inodes.add(inode)
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=True):
            safe_walk(entry.path)
```

**Structured error on loop detection:**
```json
{
  "ok": false,
  "error": {
    "code": "SYMLINK_LOOP",
    "message": "Circular symlink detected at /tmp/a/link_to_b/link_to_a.",
    "path": "/tmp/a/link_to_b/link_to_a",
    "loop_target": "/tmp/a",
    "completed_count": 42,
    "hint": "Use --no-follow-symlinks to skip symlinks during traversal."
  }
}
```

**For framework design:**
- Framework's filesystem traversal utilities MUST track visited inodes and exit with a structured `SYMLINK_LOOP` error (exit 4) immediately upon detection.
- `--no-follow-symlinks` flag MUST be auto-provided for all recursive traversal commands.
- Maximum traversal depth (`--max-depth`, default: 50) MUST be enforced as a second defense layer.
