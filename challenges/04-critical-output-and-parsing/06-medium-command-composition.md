> **Part I: Output & Parsing** | Challenge §6

## 6. Command Composition & Piping

**Severity:** Medium | **Frequency:** Common | **Detectability:** Easy | **Token Spend:** Medium | **Time:** Low | **Context:** Low

### The Problem

Agents often need to chain commands: get an ID from one command, pass it to another. Poor composition support forces the agent to do text extraction and reformatting.

**Output not suitable for piping:**
```bash
$ tool create-user --name Alice | tool send-welcome-email
# Doesn't work: create-user outputs JSON blob, send-welcome-email expects a user ID
```

**Required format transformation between commands:**
```bash
$ ID=$(tool get-user --name Alice --output json | python -c "import sys,json; print(json.load(sys.stdin)['id'])")
$ tool delete-user --id $ID
# Agent has to know the JSON structure and write extraction logic
```

**Commands that don't read from stdin:**
```bash
$ tool get-user-id --name Alice | tool send-email
# send-email ignores stdin, requires --user-id argument
```

### Solutions

**`--output id` mode (extract single value):**
```bash
$ tool get-user --name Alice --output id
42
# Just the primary identifier, no JSON, pipeable
```

**Stdin acceptance for IDs:**
```bash
$ tool get-user --name Alice --output id | tool send-welcome-email --user-id -
# --user-id - means "read from stdin"
```

**Batch input from file/stdin:**
```bash
$ tool list-users --output jsonl | tool send-welcome-email --users-jsonl -
```

**`--from` flag for reading prior command output:**
```bash
$ tool get-user --name Alice --output json > /tmp/user.json
$ tool send-welcome-email --from-file /tmp/user.json
```

**For framework design:**
- Every command that takes an ID also accepts `-` to read from stdin
- Provide `--output id` as a standard extraction mode
- Define a pipe protocol: each framework command can declare what it emits and what it accepts
