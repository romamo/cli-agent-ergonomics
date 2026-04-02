# REQ-F-071: File Descriptor Leak Prevention

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** Silent assumption — agents assume tools that exec subprocesses do not leak open file descriptors into the child; leaked fds cause EOF hangs when the subprocess inherits an open pipe to the agent's stdout

**Addresses:** Severity: High / Token Spend: High / Time: Critical / Context: Low

---

## Description

The framework MUST set the close-on-exec flag (`O_CLOEXEC` on POSIX, `HANDLE_FLAG_INHERIT=0` on Windows) on all file descriptors it opens — config files, log files, lock files, temp files, socket connections, and pipe handles. When the framework spawns subprocesses, it MUST use the language runtime's close-fds equivalent (`close_fds=True` in Python subprocess, `CLOEXEC` in Go `exec.Cmd`, `stdio: 'ignore'` for unused streams in Node.js).

A subprocess that inherits an open pipe to the parent's stdout will keep that pipe open after the parent tool process exits. The agent's read loop waiting on that pipe never receives EOF and hangs indefinitely — a Critical time impact, hard to diagnose.

## Acceptance Criteria

- After a command exits, no file descriptors opened by the framework remain open in any surviving child processes
- `lsof -p <child_pid>` after parent exit shows no inherited framework-opened fds
- Framework-spawned subprocesses inherit only stdin, stdout, and stderr (or explicitly declared fds)
- O_CLOEXEC (or equivalent) is set on open() calls in all framework file utilities
- Verified with: spawn a child that sleeps 60s; kill parent; child must not hold any framework fds open

---

## Schema

No dedicated schema type — this requirement governs subprocess spawning behavior

---

## Wire Format

No wire format change — this is an implementation constraint on process spawning

---

## Example

Without this requirement (broken):
```
agent reads stdout of: tool pipeline | head -n 5
tool exits after 5 lines
tool's internal worker subprocess (started without O_CLOEXEC) still holds stdout pipe open
head -n 5 has its data but pipe is not closed
agent read loop hangs indefinitely waiting for EOF
```

With this requirement (correct):
```
tool exits → all fds closed-on-exec → worker subprocess has no inherited stdout pipe
→ pipe closes → head -n 5 exits → agent read loop completes normally
```

---

## Related

| Requirement | Tier | Relationship |
|-------------|------|--------------|
| [REQ-F-030](f-030-child-process-session-tracking.md) | F | Provides: session tracking used to enumerate children for fd audit |
| [REQ-F-031](f-031-sigterm-forwarding-to-tracked-children.md) | F | Extends: SIGTERM forwarding requires knowing which children hold fds |
| [REQ-F-053](f-053-stdout-unbuffering-in-non-tty-mode.md) | F | Composes: stdout unbuffering and fd cleanup together prevent pipe hangs |
