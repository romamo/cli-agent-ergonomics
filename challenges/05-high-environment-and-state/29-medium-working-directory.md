> **Part V: Environment & State** | Challenge §29

## 29. Working Directory Sensitivity

**Severity:** Medium | **Frequency:** Common | **Detectability:** Medium | **Token Spend:** Medium | **Time:** Low | **Context:** Low

### The Problem

Many CLI tools resolve paths, find config files, or change behavior based on the current working directory. Agents set CWD at session start and may not realize that CWD matters for a given command — or that the correct CWD differs per command.

**Implicit project root discovery:**
```bash
$ cd /project/src/components && tool build
# Tool walks up to find package.json → /project/package.json
# Builds from /project, not /project/src/components
# Output paths are relative to /project
# Agent expected paths relative to /project/src/components
```

**Config file discovered from CWD:**
```bash
$ tool validate
# Looks for .toolrc in CWD, then parent dirs
# Agent's CWD=/tmp → no .toolrc found → uses global defaults
# Behavior differs from running in /project where .toolrc exists
```

**Relative paths in output:**
```bash
$ cd /project && tool list-files
{"files": ["src/index.ts", "src/utils.ts"]}
# Paths are relative to CWD at time of call
# Agent stores these, later calls tool from different CWD
# Paths are now wrong
```

**`cd` side effects across tool calls:**
```bash
# Agent calls: tool set-context --dir /project
# Tool internally does os.chdir("/project")
# Next tool call: CWD has changed, agent doesn't know
```

### Impact

- Different CWD → different config loaded → different behavior
- Relative paths in output become stale or wrong
- Tool finds wrong project root, operates on wrong codebase
- Silent failures: command succeeds but affects wrong files

### Solutions

**Always output absolute paths:**
```json
{
  "files": [
    "/project/src/index.ts",
    "/project/src/utils.ts"
  ]
}
```

**Include CWD used in `meta`:**
```json
{
  "meta": {
    "cwd": "/project",
    "project_root": "/project"
  }
}
```

**Explicit `--cwd` / `--root` flag:**
```bash
tool build --cwd /project
tool validate --root /project
# CWD-independent: agent always passes explicit path
```

**Never mutate CWD of the calling process:**
```python
# Bad: os.chdir(target_dir)
# Good: use absolute paths internally; never change process CWD
import os
old_cwd = os.getcwd()
# operate with absolute paths throughout
```

**For framework design:**
- All path outputs are absolute by default
- `meta.cwd` included in every response
- `--cwd` flag available on all commands as a framework standard
- Framework never calls `os.chdir()` / `process.chdir()`
