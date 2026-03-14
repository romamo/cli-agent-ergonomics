> **Part V: Environment & State** | Challenge §27

## 27. Platform & Shell Portability

**Severity:** Medium | **Frequency:** Common | **Detectability:** Easy | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

Agent environments vary: macOS, Linux, Docker containers, CI runners. Shell assumptions and platform-specific behavior cause silent failures on non-target platforms.

**macOS vs Linux differences:**
```bash
$ sed -i 's/foo/bar/' file.txt
# Linux: works
# macOS: Error: invalid command code 's'
# macOS requires: sed -i '' 's/foo/bar/' file.txt
```

**Shell-specific syntax:**
```bash
$ tool --args "key=value key2=value2"
# Works in bash
# Fails in sh (no word splitting override)
# Behaves differently in zsh
```

**Path assumptions:**
```bash
#!/usr/bin/env python3
# Assumes python3 in PATH — not true in all containers
```

**GNU vs BSD tool flags:**
```bash
date --iso-8601   # GNU date
date -u +%Y-%m-%dT%H:%M:%SZ  # portable
```

### Solutions

**Portable shebang and runtime detection:**
```bash
#!/usr/bin/env -S python3 -u
# -S: allows arguments after env command (GNU env >=8.30 / macOS 12+)
```

**Explicit shell and version requirements:**
```json
{
  "requires": {
    "shell": "bash>=4.0",
    "platform": ["linux", "darwin"],
    "tools": ["curl>=7.0", "jq>=1.6"]
  }
}
```

**For framework design:**
- `tool doctor` checks platform compatibility
- Framework abstracts platform differences (dates, paths, colors)
- All paths use forward slashes, never backslash (for cross-platform scripts)
