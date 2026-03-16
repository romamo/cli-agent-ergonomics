> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §45

## 45. Headless Authentication / OAuth Browser Flow Blocking

**Severity:** Critical | **Frequency:** Common | **Detectability:** Hard | **Token Spend:** High | **Time:** Critical | **Context:** Low

### The Problem

Many modern CLI tools implement authentication via OAuth flows that require a browser — typically an OAuth authorization code flow where the CLI opens a browser tab, the user logs in, and the browser redirects back to a localhost callback server. In agent environments, there is no browser, no desktop, and often no display server. The tool hangs waiting for a browser interaction that will never occur.

This is distinct from challenge #24 (Authentication & Secret Handling), which covers secret storage and env var loading. This challenge covers the *authentication flow initiation* — the step before secrets exist — which blocks agent use entirely.

```bash
# Agent tries to use a CLI tool for the first time
$ gh auth login
# CLI: "Press Enter to open github.com in your browser..."
# Agent sends Enter
# CLI: "Opening browser... Waiting for authentication..."
# No browser available in agent environment → hangs forever
```

Common failure patterns:
1. **OAuth authorization code flow**: CLI opens browser, waits for redirect to localhost
2. **Device code flow** (better but still problematic): CLI prints a URL and a code, waits for the user to visit the URL and enter the code — agent cannot do this autonomously
3. **Interactive token entry**: CLI prompts "Enter your API token:" — blocks on stdin (challenge #10) but specifically in an auth context where the token isn't pre-provided
4. **Credential file expiry**: CLI has stored credentials but they have expired; re-auth requires the browser flow; agent gets auth errors with no clear fix

The MCP HTTP transport requires OAuth 2.1 with PKCE, which is correct for security but adds significant complexity for agent environments that need pre-authorized service accounts or pre-issued tokens.

### Impact

- Complete authentication failure in headless agent environments.
- No structured error output: many tools just hang waiting for the browser (challenge #10 compound).
- Even if the agent detects the hang and kills the process, it has no machine-readable information about what authentication mechanism to use.
- Expired credentials produce auth errors that are indistinguishable from permission errors without a structured error code.
- Single-sign-on and enterprise SSO flows are particularly problematic: they may require multi-factor authentication that is inherently interactive.

### Solutions

**For CLI authors:**
```python
# Check for non-interactive auth options before attempting browser flow
if not sys.stdin.isatty():
    # Non-interactive mode: check for token in env vars
    token = os.environ.get("MY_TOOL_TOKEN") or os.environ.get("MY_TOOL_API_KEY")
    if not token:
        print(json.dumps({"ok": False, "error": {
            "code": "AUTH_REQUIRED",
            "message": "No credentials found. Set MY_TOOL_TOKEN environment variable.",
            "auth_methods": [
                {"type": "env_var", "name": "MY_TOOL_TOKEN", "description": "API token"},
                {"type": "env_var", "name": "MY_TOOL_API_KEY", "description": "Legacy API key"}
            ]
        }}))
        sys.exit(8)  # PERMISSION_DENIED exit code
    authenticate_with_token(token)
else:
    # Interactive: offer browser flow
    launch_browser_auth_flow()
```

**For framework design:**
- Any command that triggers authentication must check `isatty()` and return a structured `AUTH_REQUIRED` error in non-interactive mode, never hang.
- The `AUTH_REQUIRED` error must include `auth_methods` — an array of structured objects describing how to authenticate non-interactively (env var name, config file format, token endpoint).
- Schema output should include `"requires_auth": true` and `"auth_methods": [...]` so agents can determine how to authenticate before first invocation.
- Support `--token` / `--api-key` as universal authentication flags that bypass stored credentials for headless use.
- Credential expiry should produce `{"code": "AUTH_EXPIRED"}` distinct from `AUTH_REQUIRED`, with instructions for renewal that work in headless mode.
