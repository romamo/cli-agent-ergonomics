> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §68

## 68. Third-Party Library Stdout Pollution

**Source:** Gemini `02_output_context.md`, Antigravity `01_io_and_formatting.md` (RA)

**Severity:** High | **Frequency:** Common | **Detectability:** Medium | **Token Spend:** Medium | **Time:** Low | **Context:** High

### The Problem

Distinct from §3 (command author stream discipline) and §41 (update notifiers), this challenge is about deeply embedded SDK dependencies, database drivers, analytics libraries, and telemetry agents that call `print()` / `console.log()` / `fmt.Println()` directly, bypassing the CLI framework's output routing entirely. These writes cannot be suppressed via `NO_COLOR`, `CI=1`, `--quiet`, or the framework's own output controls — they go directly to file descriptor 1. The result is stdout contaminated with prose that breaks agent JSON parsing.

```python
# Tool imports a database driver that logs on connect:
import psycopg2  # on import, may print version info
conn = psycopg2.connect(...)  # prints: "psycopg2 connected to postgres://... [SSL enabled]"

# Analytics SDK fires on import:
import my_analytics_sdk  # prints: "Analytics initialized. Session: abc123"

# Both print to stdout directly — tool author has no control
```

```bash
$ my-tool list-users --output json
Analytics initialized. Session: abc123
psycopg2 connected to postgres://db:5432/prod [SSL enabled]
{"ok": true, "data": [...]}
# JSON parser sees: "Analytics initialized..." — not valid JSON → crash
```

The tool author may not even know these prints are happening (buried in a dependency 3 levels deep, or activated only in certain environments).

### Impact

- JSON parser crashes on first line of stdout contaminated with prose
- Agent receives unparseable output with no indication of which dependency polluted it
- Suppression is impossible via normal CLI flags — requires framework-level interception
- Problem can appear inconsistently (only in some environments, only with certain dependency versions)

### Solutions

**Framework-level stdout interception:**
```python
import sys, io

class StdoutInterceptor(io.TextIOWrapper):
    def write(self, data):
        if self._json_mode and not self._in_framework_output:
            # Route to stderr instead of stdout
            sys.stderr.write(f"[INTERCEPTED STDOUT]: {data}")
        else:
            super().write(data)

# Install before any imports:
sys.stdout = StdoutInterceptor(sys.stdout.buffer)
```

**Buffer stdout, validate before flushing:**
```python
# Collect all stdout writes; on command completion, validate that
# the buffer is valid JSON. If not, separate legitimate output from
# pollution and emit pollution as warnings[].
```

**Intercept at the file descriptor level:**
```python
import os
# Redirect fd 1 to a buffer; only framework's output() call writes to original fd 1
old_stdout_fd = os.dup(1)
os.dup2(pipe_write_fd, 1)
# After command completes, read buffer, filter non-JSON lines, emit as warnings
```

**For framework design:**
- Framework MUST intercept `sys.stdout` (Python) or `process.stdout` (Node.js) at startup, buffering all writes not made through the framework's `output()` API.
- Any stdout writes not from `output()` MUST be reclassified: moved to `warnings[]` if they are prose, or dropped with a `THIRD_PARTY_STDOUT` warning in debug mode.
- Framework MUST install the interceptor before any imports so that import-time prints are captured.
