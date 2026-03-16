> **Part I: Output & Parsing** | Challenge §4

## 4. Verbosity & Token Cost

**Severity:** Medium | **Frequency:** Very Common | **Detectability:** Easy | **Token Spend:** High | **Time:** Low | **Context:** High

### The Problem

Every byte of CLI output that reaches the agent consumes tokens from its context window. Verbose tools directly increase cost per operation and reduce how many operations fit in a context window.

**Verbose output that wastes tokens:**
```bash
$ tool list-files --dir /project
Scanning directory /project...
Found 1,247 files across 89 directories
Analyzing file types...
  JavaScript: 342 files
  TypeScript: 289 files
  CSS: 45 files
  HTML: 12 files
  JSON: 156 files
  Markdown: 23 files
  Other: 380 files
Summary:
  Total size: 45.2 MB
  Largest file: dist/bundle.js (2.1 MB)
  Newest file: src/components/Button.tsx (modified 2 hours ago)
  Oldest file: README.md (modified 3 years ago)
Scan completed in 0.34 seconds.
```

The agent probably just needed file paths. All the analysis text is noise.

**Debug output leaking into normal runs:**
```bash
$ tool deploy
[DEBUG] Loading config from /home/user/.config/tool/config.toml
[DEBUG] Resolving endpoint: api.example.com → 1.2.3.4
[DEBUG] Establishing connection...
[DEBUG] Sending request: POST /v1/deploy
[DEBUG] Response: 200 OK
Deployed successfully.
```

**Redundant confirmation messages:**
```bash
$ tool create-user --name Alice
User creation initiated.
Processing user Alice...
User Alice has been created successfully with ID 42.
Your new user Alice is ready to use.
Have a great day!
```

### Impact

- Directly increases $/operation
- Reduces effective context window for reasoning
- Signal-to-noise ratio forces agent to spend tokens filtering irrelevant content
- Accumulated across many tool calls, verbose tools can exhaust context

### Solutions

**Tiered verbosity:**
```bash
tool deploy --quiet          # only emit final JSON result, no prose
tool deploy                  # default: minimal human output + JSON
tool deploy --verbose        # progress to stderr, JSON to stdout
tool deploy --debug          # full debug trace to stderr
```

**`CI` environment auto-detection:**
```bash
# When CI=true, behave as --quiet automatically
if [ "$CI" = "true" ]; then
  VERBOSITY=quiet
fi
```

**Minimal JSON output by default:**
```json
// Bad default: everything
{"id": 42, "name": "Alice", "email": "alice@example.com", "created_at": "...",
 "updated_at": "...", "role": "user", "preferences": {...}, "metadata": {...}}

// Good default: just what was asked for
{"id": 42, "name": "Alice"}

// With --full flag: everything
```

**`--fields` selector:**
```bash
tool list-users --fields id,name --output json
# Returns only requested fields
```

**For framework design:**
- Default verbosity is `--quiet` when stdout is not a TTY
- JSON output never includes prose, only structured data
- Provide `--fields` filtering at framework level
- Track and log token-approximate output sizes for monitoring
