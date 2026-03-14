> **Part II: Execution & Reliability** | Challenge §10

## 10. Interactivity & TTY Requirements

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Critical | **Context:** Low

### The Problem

Agents run in non-interactive environments. Any command that requires a TTY or user input will hang indefinitely, consuming the agent's timeout budget or blocking the entire pipeline.

**Commands that hang without TTY:**
```bash
$ git commit          # opens $EDITOR — hangs forever
$ sudo apt install x  # prompts for password — hangs
$ npm init            # interactive wizard — hangs
$ ssh user@host       # may prompt for host key confirmation
$ gpg --gen-key       # interactive key generation — hangs
$ less output.txt     # opens pager — hangs
$ python              # REPL — hangs
```

**Conditional interactivity (hardest to detect):**
```bash
$ tool deploy
# If config exists: runs silently
# If config missing: opens interactive wizard
# Agent cannot know which branch will execute
```

**Hidden interactivity via pagers:**
```bash
$ git log          # pipes to `less` if output > terminal height
$ man command      # always opens pager
# PAGER=cat fixes this but agents don't always know to set it
```

**Password/confirmation prompts that look like hangs:**
```bash
$ tool delete-all-data
Are you sure? (yes/no):
# stdin is /dev/null in agent context
# tool waits forever for input that never comes
```

### Impact

- Agent's turn times out, task fails with no actionable error
- Subsequent pipeline steps never execute
- Hard to debug — logs show the command started but never finished

### Solutions

**Always provide non-interactive flags:**
```bash
tool deploy --non-interactive
tool deploy --yes          # auto-confirm all prompts
tool deploy --no-input     # fail immediately if input would be needed
tool init --defaults       # use defaults, skip all prompts
```

**Detect non-interactive context and adapt:**
```python
import sys
if not sys.stdin.isatty():
    # non-interactive mode: use defaults, fail on ambiguity
    # never prompt
```

**Fail fast instead of hanging:**
```bash
$ tool deploy --no-input
Error: Config file not found. Run `tool init` first or provide --config.
exit 4   # precondition not met
# ← agent gets an immediate, actionable error instead of a hang
```

**For framework design:**
- Auto-detect `sys.stdin.isatty()` and set `--non-interactive` implicitly
- Never use pagers; respect `NO_COLOR`, `TERM=dumb`, `CI` env vars
- Any command with a confirmation prompt MUST have a `--yes`/`--force` flag
- Document which commands are interactive in help text
- Set `PAGER=cat` and `GIT_PAGER=cat` in agent execution environments

---

> **Merged from §36:** The following content was originally a separate challenge.
> It is consolidated here because it describes a specific case of the same root problem.

### Subsection: Pager Invocation Blocking Agent Pipelines

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Critical | **Context:** Low

### The Problem

Many CLI frameworks include built-in pager support — `click.echo_via_pager()`, `git log` opening `less`, `man` pages — which spawns an interactive pager process (`less`, `more`, `$PAGER`) that waits for keyboard input. When an agent invokes a command that triggers a pager, the agent's subprocess hangs indefinitely waiting for keyboard navigation input that will never arrive.

```python
# In a Click-based tool — looks harmless, destroys agent invocation
@app.command()
def show_log():
    logs = get_all_logs()  # returns 500 lines
    click.echo_via_pager('\n'.join(logs))  # spawns 'less', blocks forever
```

This is distinct from challenge #10 (Interactivity & TTY Requirements), which concerns `prompt()` / `confirm()` calls waiting for keyboard answers. A pager is not asking a question — it is rendering content in a scroll-interactive display. The failure mode is also different: prompts eventually produce output on stdin; pagers silently swallow stdout and wait for `q`.

Pager invocation is especially insidious because:
1. It often only triggers when output exceeds a threshold (e.g., `git log` opens `less` only if output is longer than the terminal height).
2. The threshold is terminal-height-dependent — a test that passes in a 200-line terminal may block in a 24-line terminal simulation.
3. `PAGER` and `GIT_PAGER` environment variables control which pager is invoked; setting them to `cat` is the conventional workaround but requires knowledge of every affected tool.
4. Some tools check `isatty()` before invoking the pager; others do not and will page even when stdout is a pipe.

```bash
# Symptom: agent hangs, no output, no error
result = subprocess.run(["git", "log", "--oneline"], capture_output=True, timeout=30)
# May timeout if git detects a pseudo-TTY and opens less
```

### Impact

- Complete pipeline hang: agent waits until its own timeout expires (challenge #11), wasting the full timeout budget.
- No error output: the pager process may not produce any stderr or exit code until killed.
- Inconsistent behavior: same command may page in one environment and not another, making the problem hard to reproduce.
- Silent token waste: agent loop burns time without making progress.
- Downstream tools in a pipeline receive nothing if the pager captures all stdout.

### Solutions

**For agents invoking CLI tools:**
```python
import os, subprocess

# Set pager to cat universally before any subprocess
env = {**os.environ, "PAGER": "cat", "GIT_PAGER": "cat", "MANPAGER": "cat", "LESS": "-FRX"}
result = subprocess.run(cmd, env=env, capture_output=True, timeout=30)
```

**For CLI authors:**
```python
# Never use echo_via_pager() in any code path reachable by non-TTY callers
import sys
if sys.stdout.isatty():
    click.echo_via_pager(content)  # only for human terminals
else:
    click.echo(content)  # direct output for agents/pipes
```

**For framework design:**
- Ban `echo_via_pager()` and equivalent calls at the framework level; require authors to use a `output(content, paginate=True)` API that the framework conditionally paginates based on TTY detection.
- Set `PAGER=cat` in the process environment at framework initialization when `isatty(stdout) == False`.
- Never invoke external pagers from within the framework's own help or error display.
- Provide a linter / framework-level assertion that fails at command registration if any registered command's code path calls `echo_via_pager` unconditionally.
