> **Part III: Errors & Discoverability** | Challenge §21

## 21. Schema & Help Discoverability

**Severity:** Medium | **Frequency:** Very Common | **Detectability:** Easy | **Token Spend:** High | **Time:** Medium | **Context:** Medium

### The Problem

Agents need to know what commands exist, what parameters they accept, and what they return — without running commands to discover this. Human-formatted help text is expensive to parse.

**Help text only in human format:**
```bash
$ tool --help
Usage: tool [OPTIONS] COMMAND [ARGS]...

Options:
  --verbose  Enable verbose output
  --help     Show this message and exit.

Commands:
  deploy   Deploy the application
  rollback Rollback to previous version
```

**No machine-readable schema:**
```bash
$ tool deploy --help
# Returns prose. Agent has to parse natural language to understand args.
```

**No output schema:**
```bash
# Agent has no way to know what fields deploy will return without running it
```

### Solutions

**Machine-readable command manifest:**
```bash
$ tool --schema --output json
{
  "commands": [
    {
      "name": "deploy",
      "description": "Deploy the application to an environment",
      "danger_level": "mutating",
      "parameters": [
        {"name": "env", "type": "string", "required": true,
         "enum": ["staging", "prod"], "description": "Target environment"},
        {"name": "version", "type": "string", "required": false,
         "description": "Version tag to deploy (default: latest)"},
        {"name": "dry-run", "type": "boolean", "default": false}
      ],
      "output_schema": {
        "type": "object",
        "properties": {
          "ok": {"type": "boolean"},
          "effect": {"type": "string", "enum": ["deployed", "noop"]},
          "data": {
            "deployment_id": {"type": "string"},
            "version": {"type": "string"}
          }
        }
      },
      "exit_codes": {
        "0": "success",
        "1": "deployment failed",
        "4": "environment not found",
        "7": "deployment timed out"
      }
    }
  ]
}
```

**For framework design:**
- Every command auto-generates its schema from its parameter declarations
- `tool --schema` outputs the full manifest
- Output schema is declared alongside input schema, not separate
- Schema versioning: `tool --schema-version` to track evolution
