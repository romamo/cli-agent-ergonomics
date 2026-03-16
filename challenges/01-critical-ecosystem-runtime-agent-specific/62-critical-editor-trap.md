> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §62

## 62. $EDITOR and $VISUAL Trap

**Source:** Gemini `03_execution_flow.md`, Antigravity `02_interactivity_and_prompts.md` (RA)

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Critical | **Context:** Low

### The Problem

Distinct from §37 (REPL triggering), many CLI tools invoke the user's `$EDITOR` or `$VISUAL` environment variable to open a text editor for structured input: `git commit` (without `-m`), `kubectl edit`, `crontab -e`, `visudo`, `tool config edit`. In non-TTY mode, these editor invocations either block indefinitely (vim waits for input), emit a flood of raw escape sequences, or crash with a tty-related error — all of which halt the agent.

```bash
# Agent runs git commit expecting to provide the message programmatically
$ git commit
# $EDITOR=vim is launched
# vim writes: \x1b[?1049h\x1b[22;0;0t\x1b[1;40r... (terminal init sequences)
# vim then blocks on stdin waiting for keystrokes
# In non-TTY mode: either hangs or immediately exits with "Vim: Warning: Input is not from a terminal"
# Either way: agent gets no commit

# kubectl edit opens $EDITOR with current resource YAML
$ kubectl edit deployment/my-app
# Opens vim with 200 lines of YAML
# Agent cannot edit the file and save it
# kubectl waits indefinitely for the editor to exit
```

### Impact

- Agent blocked indefinitely waiting for editor to complete
- Raw terminal escape sequences from editor startup contaminate any captured output
- The operation requiring the editor (commit, resource update) cannot proceed
- Agent has no way to know this will happen until after the blocking call

### Solutions

**Provide non-editor alternatives for all editor-requiring operations:**
```bash
# Good: explicit content flag bypasses editor
$ git commit -m "message"
$ kubectl patch deployment/my-app --patch '{"spec": {...}}'
$ tool config set key=value   # instead of tool config edit
```

**Set $EDITOR to a non-blocking shim in non-TTY mode:**
```bash
# Framework sets: EDITOR="tee /dev/stderr" or EDITOR="cat > /dev/null"
# Or: EDITOR="my-tool-editor-shim" which reads content from --editor-content flag
```

**Detect editor invocation in non-TTY mode and fail fast:**
```json
{
  "ok": false,
  "error": {
    "code": "EDITOR_REQUIRED",
    "message": "This command requires an interactive editor. Use --message or --from-file instead.",
    "alternatives": ["git commit -m '<message>'", "git commit --file <path>"]
  }
}
```

**For framework design:**
- Framework MUST set `EDITOR=true` (a no-op) and `VISUAL=true` in the subprocess environment when in non-TTY mode, preventing any spawned subprocess from launching an interactive editor.
- Commands that use `$EDITOR` MUST declare `requires_editor: true` in their schema and provide a `--content` or `--from-file` alternative for non-TTY operation.
- Framework MUST detect editor invocations in non-TTY mode and intercept them with exit 4 and a structured error listing the non-interactive alternative.
