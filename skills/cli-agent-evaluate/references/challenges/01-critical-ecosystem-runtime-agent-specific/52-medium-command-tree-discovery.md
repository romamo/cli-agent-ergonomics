> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §52

## 52. Recursive Command Tree Discovery Cost

**Severity:** Medium | **Frequency:** Very Common | **Detectability:** Easy | **Token Spend:** High | **Time:** Medium | **Context:** High

### The Problem

Most CLIs require N+1 help calls to discover the full command surface: one call to list top-level subcommands, then one more call per subcommand to see its flags. A tool with 20 subcommands requires 21 sequential round trips just to build a mental model before any real work begins. With 3+ levels of nesting (`tool resource type action --flags`), the discovery cost grows exponentially. There is no standard for returning the full command tree in a single structured call.

```bash
$ tool --help
# Shows: create, list, update, delete, config, auth, export  ← 7 subcommands

$ tool create --help     # call 2
$ tool list --help       # call 3
$ tool update --help     # call 4
$ tool delete --help     # call 5
$ tool config --help     # call 6
$ tool config get --help # call 7 — subcommand of subcommand
$ tool config set --help # call 8
# ... 8+ calls just to see all flags, before any work starts

# Deep nesting:
$ aws ec2 describe-instances --help    # 3 levels deep
# Discovering the full aws CLI surface: hundreds of calls
```

The problem compounds when the agent must select the right command for a task — it needs to see all available commands before choosing, which means paying the full discovery cost upfront.

### Impact

- 10–50+ tool calls burned on discovery before first productive call
- Full command tree may consume a large fraction of the context window when retrieved incrementally
- Agent may miss relevant subcommands it didn't know to ask about
- Cached command trees go stale after tool updates; no standard way to detect staleness

### Solutions

**Single-call full tree export:**
```bash
$ tool --schema --full
```
```json
{
  "tool": "my-tool",
  "version": "1.2.3",
  "schema_version": "1.0",
  "commands": [
    {
      "name": "create",
      "description": "Create a new resource",
      "args": [],
      "flags": [],
      "subcommands": []
    },
    {
      "name": "config",
      "subcommands": [
        { "name": "get", "args": [] },
        { "name": "set", "args": [] }
      ]
    }
  ]
}
```

**For framework design:**
- `tool --schema` (REQ-O-013) MUST return the full command tree by default, not just the top-level command.
- Each command node in the tree includes: name, description, args with types and constraints, flags, required/optional status, subcommands.
- The full schema export must be a single synchronous call completing in under 500ms regardless of command count.
