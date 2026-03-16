> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §54

## 54. Conditional / Dependent Argument Requirements

**Severity:** High | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Medium | **Context:** Low

### The Problem

Many commands have arguments only required when another argument takes a specific value: `--auth-type oauth` requires `--client-id` and `--client-secret`; `--output file` requires `--output-path`. These conditional dependencies are almost never expressed in machine-readable form. The agent provides a partial set of arguments, the tool fails, and the agent must retry — often multiple times, discovering one missing co-requirement per round trip.

```bash
# Round trip 1
$ tool create --type oauth
Error: missing required argument: --client-id

# Round trip 2
$ tool create --type oauth --client-id abc123
Error: missing required argument: --client-secret

# Round trip 3: finally works — but took 3 calls to discover a 2-flag dependency
$ tool create --type oauth --client-id abc123 --client-secret xyz
```

### Impact

- N round trips to discover N co-required arguments in a dependency group
- Mid-execution failures for implicit conditional requirements not in the schema
- Agent cannot pre-validate a complete invocation without undocumented domain knowledge

### Solutions

**Schema declares conditional requirement groups:**
```json
{
  "arg_groups": [
    {
      "condition": {"arg": "auth-type", "equals": "oauth"},
      "required": ["client-id", "client-secret"]
    }
  ]
}
```

**Phase 1 validation reports ALL missing co-requirements at once:**
```json
{
  "ok": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "missing_args": [
      {"name": "client-id", "reason": "required when --auth-type=oauth"},
      {"name": "client-secret", "reason": "required when --auth-type=oauth"}
    ]
  }
}
```

**For framework design:**
- Schema format MUST support `required_when` and `arg_groups` conditional dependency declarations.
- Phase 1 validation MUST evaluate all conditional requirements simultaneously and report all missing args in a single error response.
