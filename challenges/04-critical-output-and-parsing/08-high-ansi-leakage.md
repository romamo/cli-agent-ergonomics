> **Part I: Output & Parsing** | Challenge §8

## 8. ANSI & Color Code Leakage

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** Medium | **Time:** Low | **Context:** Medium

### The Problem

ANSI escape sequences (colors, bold, cursor movement) are designed for TTY display. When they leak into non-TTY output, they corrupt JSON, break regex matching, and inflate token count with invisible garbage.

**Color codes in JSON output:**
```bash
$ tool get-status --output json
\e[32m{"ok": true, "status": "healthy"}\e[0m
# JSON parser: fails or returns string starting with ESC character
# Agent sees: invalid JSON
```

**Partial color disable:**
```bash
$ tool list-users --no-color
# Removes text colors but keeps:
# - Bold sequences: \e[1m ... \e[0m
# - Cursor movement: \e[2K (erase line)
# - Progress bar resets: \r\e[A
# Agent still receives corrupted output
```

**Color in error messages:**
```bash
$ tool deploy 2>&1
\e[31mError:\e[0m deployment failed
# Agent captures stderr+stdout combined
# Error parsing: "ESC[31mError:ESC[0m" — pattern matching fails
```

**Library-level color injection:**
```bash
# Tool uses a logging library that auto-enables color
# Tool author didn't know it was happening
# NO_COLOR env var not respected by the library
```

### Impact

- JSON parse failure — agent gets no structured data
- Regex/string matching fails on error codes or status values
- Token waste — escape sequences consume tokens with zero information value
- Inconsistent behavior: works in dev (TTY), breaks in CI/agent (non-TTY)

### Solutions

**Auto-detect non-TTY and disable all sequences:**
```python
import sys, os

def should_use_color() -> bool:
    if os.environ.get("NO_COLOR"):        return False
    if os.environ.get("TERM") == "dumb":  return False
    if os.environ.get("CI"):              return False
    if not sys.stdout.isatty():           return False
    return True
```

**Strip escape codes from all output in `--output json` mode — unconditionally:**
```python
import re

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\][^\x07]*\x07|\r')

def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub('', text)

# Apply to ALL strings before JSON serialization, not just terminal output
```

**Respect the NO_COLOR standard (no-color.org):**
```python
# Check NO_COLOR before any color output
# NO_COLOR presence (any value, including empty) = disable color
if "NO_COLOR" in os.environ:
    disable_all_color()
```

**Audit third-party libraries:**
```python
# Force-disable color in common libraries:
os.environ["NO_COLOR"] = "1"          # universal
os.environ["FORCE_COLOR"] = "0"       # some node tools
os.environ["TERM"] = "dumb"           # fallback
os.environ["ANSIBLE_FORCE_COLOR"] = "0"
```

**For framework design:**
- Framework sets `NO_COLOR=1` automatically when stdout is not a TTY
- All string values pass through `strip_ansi()` before JSON serialization
- `--output json` mode unconditionally disables color regardless of TTY state
- Framework CI detection: `CI`, `GITHUB_ACTIONS`, `JENKINS_URL` → auto-quiet
