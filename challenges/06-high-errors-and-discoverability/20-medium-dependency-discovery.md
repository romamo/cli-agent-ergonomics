> **Part III: Errors & Discoverability** | Challenge §20

## 20. Environment & Dependency Discovery

**Severity:** Medium | **Frequency:** Common | **Detectability:** Easy | **Token Spend:** Medium | **Time:** Medium | **Context:** Low

### The Problem

CLI tools often depend on external tools, services, or specific environment configurations. When these are missing, the failure message doesn't tell the agent what's missing or how to get it.

**Unhelpful missing dependency errors:**
```bash
$ tool build
/bin/sh: docker: command not found
exit 127
# Agent knows docker is missing but not: which version, how to install,
# whether there's an alternative
```

**Silent wrong version usage:**
```bash
$ tool deploy
Deploying...
Error: unsupported field 'replicas' in deployment spec
exit 1
# Actually: kubectl version is too old, but error doesn't say that
```

**Environment check scattered across execution:**
```bash
$ tool run
Connecting to DB... ok
Loading config... ok
Checking Redis... FAILED: connection refused
# Fails at step 3; agent has to retry to discover more prereqs
```

### Solutions

**Preflight check command:**
```bash
$ tool doctor --output json
{
  "ok": false,
  "checks": [
    {"name": "docker",   "ok": true,  "version": "24.0.5", "required": ">=20.0"},
    {"name": "kubectl",  "ok": false, "found": "1.18.0", "required": ">=1.24",
     "fix": "brew upgrade kubectl"},
    {"name": "db_conn",  "ok": true},
    {"name": "redis",    "ok": false, "error": "connection refused at localhost:6379",
     "fix": "docker run -d redis"}
  ]
}
```

**Dependency declaration in help:**
```bash
$ tool build --show-requirements --output json
{
  "required": [
    {"name": "docker", "version": ">=20.0", "install": "https://docs.docker.com/..."},
    {"name": "DOCKER_BUILDX_BUILDER", "type": "env_var", "optional": true}
  ]
}
```

**For framework design:**
- Framework provides a `preflight()` hook for each command
- `tool doctor` runs all preflight checks without executing any commands
- Each failed check includes a `fix` field with the exact command to run
