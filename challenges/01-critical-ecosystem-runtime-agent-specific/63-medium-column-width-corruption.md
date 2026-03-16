> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §63

## 63. Terminal Column Width Output Corruption

**Source:** Antigravity `01_io_and_formatting.md` (RA)

**Severity:** Medium | **Frequency:** Common | **Detectability:** Easy | **Token Spend:** Medium | **Time:** Low | **Context:** Medium

### The Problem

Tools that format output based on terminal width (`$COLUMNS`, `shutil.get_terminal_size()`, `process.stdout.columns`) produce line-wrapped output that breaks agent parsing. A 100-character URL split across two 50-character lines becomes two invalid strings. A JSON field value containing a newline is structurally corrupt. When stdout is not a TTY, `$COLUMNS` is often unset (defaulting to 80) or inherited from a terminal with an unexpected width.

```bash
# Tool wraps long values at terminal width (80 columns by default in non-TTY):
$ tool describe resource-with-very-long-name --output json
{
  "endpoint": "https://api.very-long-subdomain.example.com/v2/resources/very-long-
path/detail",    # ← broken across two lines — invalid URL
  "description": "A resource with a long description that wraps at the terminal
width boundary"   # ← newline in string value — invalid JSON
}

# Agent tries to use the URL — fails because it's been split
# JSON parser fails on the multi-line string values
```

The problem is worse in table-formatted output (not JSON) — column alignment based on terminal width produces garbage when the terminal width assumption is wrong.

### Impact

- URLs, paths, and identifiers split across lines become invalid
- Multi-line string values corrupt JSON structure
- Table output with dynamic column widths produces unparseable garbage in non-TTY mode
- Agents receive structurally broken data with no indication of corruption

### Solutions

**Disable hard-wrapping in non-TTY mode:**
```python
# Python: don't wrap when stdout is not a TTY
import shutil, sys
columns = shutil.get_terminal_size().columns if sys.stdout.isatty() else 0
# columns=0 means "no wrap"
```

**`--width=0` flag disables all hard-wrapping:**
```bash
$ tool describe resource --width=0 --output json
# All strings output as single lines regardless of length
```

**JSON output mode MUST never hard-wrap string values:**
- In JSON output mode, the framework serializes all strings without newline injection.
- Table/human output mode may wrap; JSON output mode MUST NOT.

**For framework design:**
- Framework MUST disable all terminal-width-based formatting when JSON output mode is active.
- Framework MUST NOT inject newlines into string field values during serialization regardless of `$COLUMNS` value.
- The `--width` flag (default: `0` in non-TTY, terminal width in TTY) MUST be respected by all formatting functions.
