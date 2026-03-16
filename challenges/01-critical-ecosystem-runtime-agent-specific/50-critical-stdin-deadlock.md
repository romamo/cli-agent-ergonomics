> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §50

## 50. Stdin Consumption Deadlock

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Critical | **Context:** Low

### The Problem

Distinct from §10 (interactive prompts), some CLI tools silently read from stdin as a default fallback — not as a deliberate prompt but as an undocumented behavior: reading config from stdin when no config flag is provided, reading a list of IDs from stdin when no positional args are given, defaulting `--password` to a stdin read when the flag is omitted. In non-TTY context, this blocks indefinitely waiting for an EOF that never comes.

```bash
# Tool reads entity IDs from stdin when none are provided as args
$ my-tool delete    # agent omits the --id flag
# ← blocks forever, waiting for stdin EOF in non-TTY mode

# Password argument defaults to stdin read when omitted
$ my-tool --user admin    # agent forgets --password flag
Password:     # ← blocking read from stdin
# In non-TTY mode: hangs until timeout

# Tool falls back to reading config from stdin
$ my-tool run     # no --config flag provided
# Waiting for config JSON on stdin...
```

The tell: the process is running, consuming no CPU, producing no output — indistinguishable from "slow initialization" until the full timeout fires.

### Impact

- Agent's entire timeout budget burned silently with no error
- No warning or error is emitted before blocking occurs
- Tool may need to be killed externally, potentially leaving partial state
- If stdin is connected to a pipe, the tool may read the pipe content as its "config", corrupting input

### Solutions

**Non-TTY stdin reads must fail immediately with exit 4:**
```json
{
  "ok": false,
  "error": {
    "code": "STDIN_REQUIRED",
    "message": "Argument '--ids' requires input but stdin is not a TTY and no value was provided.",
    "hint": "Pass --ids <value> or pipe data: echo '123' | my-tool delete --ids -"
  }
}
```

**Schema must declare all stdin-reading paths:**
```json
{
  "args": [
    {
      "name": "ids",
      "stdin_fallback": true,
      "stdin_format": "newline-separated IDs",
      "non_tty_behavior": "fail_with_exit_4"
    }
  ]
}
```

**For framework design:**
- All stdin reads must be declared in the command schema; undeclared stdin reads are a framework error.
- In non-TTY mode, the framework wraps `stdin.read()` calls with an immediate-fail guard that exits 4 with a structured error listing the flag to pass instead.
- The `--schema` output for every command must indicate which args accept stdin as input and what format is expected.
