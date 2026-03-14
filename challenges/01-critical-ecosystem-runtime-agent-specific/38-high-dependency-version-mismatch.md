> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §38

## 38. Runtime Dependency Version Mismatch

**Severity:** High | **Frequency:** Common | **Detectability:** Medium | **Token Spend:** High | **Time:** High | **Context:** Low

### The Problem

CLI tools written in interpreted languages (Python, Node.js, Ruby) require specific runtime versions to be installed in the agent's execution environment. Unlike compiled binaries (Go, Rust), which are self-contained, interpreted-language tools depend on a runtime version match. When the tool requires Node 18+ but the environment has Node 16, or requires Python 3.11 but the environment has Python 3.9, the tool either fails to start (import errors, syntax errors) or exhibits subtle behavioral differences.

This is distinct from challenge #27 (Platform & Shell Portability), which addresses same-OS compatibility. Runtime version mismatch can occur on the same OS and same architecture but different runtime version.

```bash
# Agent invokes a Commander.js tool in a CI environment
$ my-node-tool analyze --input data.json
/usr/lib/node_modules/my-node-tool/node_modules/some-dep/index.js:42
  const { structuredClone } = require('v8');
  ^
SyntaxError: The requested module 'v8' does not provide an export named 'structuredClone'
# Agent sees exit 1 + cryptic Node.js internal error
# No indication that the root cause is the Node version (16 vs 18)
```

```bash
# Python: implicit dependency on f-string walrus operator requires 3.8+
$ python3 my-typer-tool.py --input data.json  # works on dev machine (3.11)
# On agent machine with Python 3.7:
SyntaxError: invalid syntax  (at position of `:=` walrus operator)
```

The problem is especially acute because:
1. Error messages reference internal module paths, not the version requirement.
2. The agent cannot distinguish a version mismatch from a bug in its input.
3. Version requirements are documented in README files, not in the CLI's error output.
4. Tools like `update-notifier` (Commander.js ecosystem) may emit version warnings to stderr before the actual command runs, interleaved with structured output.

### Impact

- Complete command failure with opaque error messages that point to runtime internals rather than the version requirement.
- Agent spends tokens attempting to fix its argument construction when the problem is environmental.
- CI/CD environments often have pinned, older runtime versions; tools work on developer machines but fail in agent environments.
- Multiple failure modes (startup crash vs. subtle behavioral difference) make consistent detection hard.
- Static binary languages (Go, Rust) do not have this problem; the asymmetry creates reliability differences across the tool ecosystem.

### Solutions

**For CLI authors:**
```python
# Python: check version at startup, emit structured error
import sys, json
MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    print(json.dumps({"ok": False, "error": {
        "code": "RUNTIME_VERSION",
        "message": f"Requires Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+, found {sys.version}",
        "requirement": f"python>={MIN_PYTHON[0]}.{MIN_PYTHON[1]}",
        "actual": sys.version
    }}))
    sys.exit(5)  # NOT_FOUND / precondition failure
```

```javascript
// Node.js: check version at top of entry file
const [major] = process.versions.node.split('.').map(Number);
if (major < 18) {
    process.stderr.write(JSON.stringify({ok: false, error: {
        code: "RUNTIME_VERSION",
        message: `Requires Node.js 18+, found ${process.versions.node}`,
    }}) + '\n');
    process.exit(5);
}
```

**For framework design:**
- Emit a structured `{"code": "RUNTIME_VERSION"}` error as the first output when minimum version check fails, before any other initialization.
- Include `"requirement"` and `"actual"` fields in the error so agents can surface the mismatch to operators.
- Expose minimum runtime requirements in `--schema` output: `"runtime": {"python": ">=3.10"}`.
- Prefer packaging tools as self-contained binaries when possible (PyInstaller, pkg for Node.js) to eliminate runtime dependency entirely.
