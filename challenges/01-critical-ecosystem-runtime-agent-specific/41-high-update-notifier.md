> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §41

## 41. Update Notifier Side-Channel Output Pollution

**Severity:** High | **Frequency:** Common (Node.js/npm ecosystem) | **Detectability:** Medium | **Token Spend:** Medium | **Time:** Medium | **Context:** Medium

### The Problem

Many widely-deployed CLI tools (particularly in the npm/Commander.js ecosystem) include `update-notifier` or equivalent libraries that:
1. Check PyPI/npm for a newer version of the tool in the background
2. Cache the result to disk (typically `~/.config/<tool>/update-check.json`)
3. Print an update notification to **stderr** (or sometimes stdout) the next time the tool is invoked

This produces unexpected, out-of-band text output at the start or end of every command invocation — text that is not part of the tool's structured output but appears in the agent's captured streams:

```
╭──────────────────────────────────────────────────────────╮
│                                                          │
│    Update available 1.2.3 → 2.0.0                       │
│    Run npm install -g my-cool-tool to update             │
│                                                          │
╰──────────────────────────────────────────────────────────╯
```

This is distinct from challenge #32 (Self-Update & Auto-Upgrade Behavior), which concerns tools that *automatically* update themselves or replace their binary during execution. Update notifiers do not modify the binary — they only print text. But that text:
- May appear before or after structured JSON output, breaking JSON parsing
- Contains ANSI box-drawing characters that violate challenge #8 constraints
- Triggers a network request on every invocation (or periodically), adding latency
- May appear on stdout (breaking data stream) or stderr (adding noise to diagnostics)

```python
# Agent captures tool output expecting JSON
result = subprocess.run(["my-cool-tool", "list", "--json"], capture_output=True)
output = result.stdout.decode()
# output might be:
# "\n\n╭─────────────────────────────────╮\n│  Update available... │\n╰───────╯\n\n[{...}]\n"
json.loads(output)  # JSONDecodeError: Extra data
```

### Impact

- JSON parsing failure when update text appears on stdout, even when the tool correctly formats its data output.
- ANSI box-drawing characters in update notifications contaminate the output stream (challenge #8 compound).
- Network request adds latency to every invocation (or at the start of a session), creating unpredictable timing.
- Agents reasoning about output must consume and discard update-notification tokens before processing actual data.
- In CI/CD environments, update notifications are irrelevant and wasteful but still fire.

### Solutions

**For agents:**
```python
env = {**os.environ, "NO_UPDATE_NOTIFIER": "1",  # npm ecosystem standard
       "CI": "true",  # suppresses update notifiers in many tools
       "DISABLE_UPDATE_NOTIFIER": "true"}  # some tools check this
result = subprocess.run(cmd, env=env, capture_output=True)
```

**For CLI authors:**
```javascript
// Check TTY and CI before enabling update notifier
const updateNotifier = require('update-notifier');
if (process.stdout.isTTY && !process.env.CI) {
    updateNotifier({pkg: require('./package.json')}).notify();
}
// Better: surface in meta.update_available field of JSON response
```

**For framework design:**
- Suppress all update notifications when `isatty(stdout) == False` or `CI == "true"`.
- If an update is available, place `"update_available": {"version": "2.0.0", "command": "npm install -g my-tool"}` in the `meta` section of the structured JSON response — never as prose on stdout or stderr.
- Never emit ANSI box-drawing characters in update notifications.
- Rate-limit update checks to once per week per installation, not once per invocation.
