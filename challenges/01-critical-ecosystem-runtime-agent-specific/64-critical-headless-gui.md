> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §64

## 64. Headless Display and GUI Launch Blocking

**Source:** Gemini `07_system_physics.md`, Antigravity `05_environment_and_execution.md` (RA)

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Critical | **Context:** Low

### The Problem

Distinct from §45 (OAuth browser flow), many CLI tools launch GUI applications for operations unrelated to authentication: opening a browser to show documentation, launching a file picker, showing a notification dialog, rendering a chart, or using X11 for visualization. In headless environments (containers, CI, SSH sessions without X11 forwarding), these launches either crash immediately (`cannot connect to X server`), hang indefinitely (waiting for a window to close), or silently do nothing while the tool waits for user interaction that never comes.

```bash
# Tool opens browser to show deployment result
$ tool deploy --env prod --open-browser
# In headless container: xdg-open hangs or crashes with:
# "Failed to open URI: No application is registered as handling this file"
# Tool is waiting for the browser to close — hangs forever

# Tool uses X11 for progress visualization
$ tool analyze --chart
# In SSH session without -X: "Error: cannot open display :0"
# Tool crashes with non-zero exit; agent doesn't know if the analyze completed

# macOS `open` command in Linux container:
$ open https://docs.example.com
# "open: command not found" → exit 127 → agent thinks deploy failed
```

### Impact

- Agent blocked indefinitely waiting for a GUI window to close
- Critical operation may have completed successfully but tool crashes during the GUI step
- Exit code reflects GUI failure, not operation result — agent can't determine if work was done
- No way for agent to know in advance which commands will attempt GUI launches

### Solutions

**Detect headless environment and skip GUI operations:**
```python
import os, sys
def is_headless():
    return (
        not sys.stdout.isatty() or
        os.environ.get('CI') or
        not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY')
    )

if is_headless():
    # Skip browser launch; emit URL in JSON instead
    return {"ok": True, "data": {"url": url, "opened": False, "open_hint": f"open {url}"}}
```

**Schema declares GUI operations:**
```json
{
  "name": "deploy",
  "gui_operations": ["browser_open"],
  "headless_behavior": "emit_url_in_output"
}
```

**Wrap graphical commands in headless fallback:**
```bash
# Tool wraps GUI launch:
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    echo '{"url": "'"$URL"'", "note": "open this URL in your browser"}'
else
    xdg-open "$URL"
fi
```

**For framework design:**
- Framework MUST detect headless environment on startup and set `framework.headless = true`.
- Commands that declare `gui_operations` MUST implement headless fallbacks; framework raises a registration error if `headless_behavior` is not declared.
- In headless mode, browser/GUI launch attempts MUST be replaced with URL/path emission in the JSON response rather than blocking.
