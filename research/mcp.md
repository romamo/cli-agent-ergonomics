# Model Context Protocol (MCP)

## Overview

Model Context Protocol (MCP) is an open, Anthropic-initiated protocol for connecting AI model applications (hosts) to external tools and data sources (servers). It was inspired by the Language Server Protocol (LSP) — the same idea applied to AI context integration rather than language-server integration. The current specification version is `2025-06-18` (date-versioned releases); the latest stable schema is `2025-11-25`.

MCP standardizes:
- How AI applications discover what tools and data a server exposes
- How they invoke those tools and retrieve that data
- How the server communicates errors, progress, and streaming updates back

MCP deliberately does **not** dictate how an AI application uses LLMs or manages the context it receives — it is a context exchange protocol only.

---

## Protocol Architecture

### Participants

| Role | Description |
|------|-------------|
| **MCP Host** | The AI application (e.g., Claude Desktop, Claude Code, VS Code) that manages one or more MCP clients |
| **MCP Client** | A connection object inside the host, one per server; maintains the dedicated channel |
| **MCP Server** | A program (local subprocess or remote HTTP service) that exposes tools, resources, and prompts |

One host can connect to many servers simultaneously, each via its own client instance.

### Layers

MCP has two layers:

**Data Layer** — JSON-RPC 2.0 message exchange:
- Lifecycle management (initialize / initialized / shutdown)
- Server primitives: tools, resources, prompts
- Client primitives: sampling, elicitation, logging, roots
- Utility primitives: progress, cancellation, pagination, notifications

**Transport Layer** — communication channel:
- **stdio**: client launches server as subprocess; stdin/stdout carry newline-delimited JSON-RPC; stderr is for logging only. Each message MUST NOT contain embedded newlines. Default for local servers.
- **Streamable HTTP**: single MCP endpoint path accepting POST (client→server) and GET (open SSE stream, server→client). Supports optional SSE streaming, resumability via `Last-Event-ID`, and session management via `Mcp-Session-Id` header. Default for remote servers.
- Custom transports are permitted if they preserve JSON-RPC message format.

### Message Format

All messages are JSON-RPC 2.0 over UTF-8. Three message types:
- **Request**: `{ "jsonrpc": "2.0", "id": <number|string>, "method": "...", "params": {...} }`
- **Response**: `{ "jsonrpc": "2.0", "id": <matching id>, "result": {...} }` or `{ ..., "error": {"code": ..., "message": "...", "data": ...} }`
- **Notification**: `{ "jsonrpc": "2.0", "method": "...", "params": {...} }` (no `id`, no response expected)

### Lifecycle

1. **Initialization**: Client sends `initialize` with `protocolVersion`, `capabilities`, `clientInfo`. Server responds with its `protocolVersion`, `capabilities`, `serverInfo`. Client sends `notifications/initialized`. Capability negotiation determines which primitives are active.
2. **Operation**: Normal message exchange within negotiated capabilities.
3. **Shutdown**: For stdio, client closes stdin then sends SIGTERM/SIGKILL. For HTTP, client closes connections or sends HTTP DELETE with `Mcp-Session-Id`.

### Server Primitives

**Tools** — callable functions:
- Defined with `name`, `title`, `description`, `inputSchema` (JSON Schema), optional `outputSchema`, optional `annotations`
- Discovered via `tools/list` (paginated with cursor)
- Invoked via `tools/call` with `{ "name": "...", "arguments": {...} }`
- Response contains `content[]` array (text/image/audio/resource_link/embedded resource) and optional `isError: true` flag; OR `structuredContent` object when `outputSchema` is provided

**Tool Annotations** (behavioral hints, advisory only, MUST be treated as untrusted unless server is trusted):
- `title`: human-readable display name
- `readOnlyHint`: if true, tool does not modify state (default: false)
- `destructiveHint`: if true, may perform destructive actions (default: true)
- `idempotentHint`: if true, repeated calls with same args have same effect (default: false)
- `openWorldHint`: if true, tool interacts with external entities beyond the server (default: true)

**Resources** — data sources:
- Identified by URI; support `file://`, `https://`, `git://`, and custom schemes
- Listed via `resources/list` (paginated); fetched via `resources/read`
- Content is either `text` (UTF-8 string) or `blob` (base64-encoded binary)
- Servers can declare `subscribe` capability to push `notifications/resources/updated`

**Prompts** — reusable templates:
- Listed via `prompts/list`; retrieved via `prompts/get` with arguments
- Return structured message arrays for injection into LLM conversations
- Designed to be user-controlled (e.g., slash commands)

### Client Primitives

**Sampling**: server requests LLM completion from client (`sampling/createMessage`) — server stays model-agnostic, client/host picks model.

**Elicitation**: server requests structured user input from client (`elicitation/create`) with a flat JSON Schema; user can accept/decline/cancel. Added in 2025-06-18 spec.

**Roots**: client exposes filesystem root URIs to servers so servers know their operating boundaries.

**Logging**: server sends log messages to client (levels: debug, info, notice, warning, error, critical, alert, emergency).

### Error Handling

Two distinct mechanisms:

1. **Protocol errors** (JSON-RPC `error` field): standard codes (-32700 parse error, -32600 invalid request, -32601 method not found, -32602 invalid params, -32603 internal error) plus MCP-specific codes (-32002 resource not found, etc.). The response has an `error` object instead of `result`.

2. **Tool execution errors** (within a successful `tools/call` result): `isError: true` in the result, with a `content` array describing the failure. This preserves the response envelope so the agent can read the error message.

### Streaming and Progress

No true token-level streaming of results; instead:
- Servers send `notifications/progress` messages with a `progressToken` (included in the original request's `_meta`), reporting fractional completion. The `progress` value must increase monotonically.
- For Streamable HTTP, the server can open an SSE stream in response to a POST, sending intermediate notifications before the final response.

### Cancellation

Either party sends `notifications/cancelled` with `{ "requestId": "...", "reason": "..." }`. The receiver SHOULD stop processing and free resources. Race conditions (response already sent) are handled gracefully — receivers MAY ignore stale cancellations. The `initialize` request cannot be cancelled.

### Session Management (Streamable HTTP)

- Server issues a cryptographically secure `Mcp-Session-Id` header in the `InitializeResult` response
- Client includes it on all subsequent requests
- Server returns 404 to invalidate a session; client must re-initialize
- Client sends HTTP DELETE to explicitly end a session
- Stream resumability via `Last-Event-ID` header for reconnection after dropped connections

### Authentication

- **stdio**: credentials come from environment (env vars, config files, OS credential stores). No protocol-level auth.
- **Streamable HTTP**: OAuth 2.1 with PKCE. Flow: server returns 401 with `WWW-Authenticate` header pointing to resource metadata URL → client discovers auth server via OAuth Protected Resource Metadata (RFC 9728) → client obtains token via OAuth Authorization Code flow → client sends `Authorization: Bearer <token>` on every request. Dynamic client registration (RFC 7591) is supported and recommended. Resource Indicators (RFC 8707) are required.

### Binary Data

Binary content is base64-encoded in JSON fields (`blob` for resources, `data` for image/audio content items). There is no raw binary framing at the protocol level.

### Pagination

`tools/list`, `resources/list`, `resources/templates/list`, `prompts/list` all support cursor-based pagination. Server includes `nextCursor` in responses; client includes `cursor` in subsequent requests. Page size is server-determined. Cursors are opaque and must not be persisted across sessions.

---

## How Agents Consume MCP Tools

From the agent's perspective (what the LLM sees and interacts with):

1. **At session start**, the host fetches all tool definitions from all connected MCP servers and presents them to the LLM as its available tool set. Each tool has a name, description, and JSON Schema for inputs. If `outputSchema` is defined, the structured output contract is also exposed.

2. **During a turn**, the LLM selects a tool by name and constructs arguments matching the `inputSchema`. The host sends `tools/call` to the appropriate server.

3. **The result** arrives as a `content[]` array of typed items (text, image, audio, resource link, embedded resource) or a `structuredContent` object. The `isError` flag signals failure-within-success. The host passes this back to the LLM as tool output.

4. **Dynamic updates**: if the server sends `notifications/tools/list_changed`, the host re-fetches `tools/list` and notifies the LLM of new capabilities.

5. **Agent never sees**: raw JSON-RPC wire format, transport details, session IDs, OAuth tokens. The host fully mediates the protocol.

6. **Sampling and elicitation**: servers can trigger nested LLM calls (sampling) or user input prompts (elicitation) mid-tool-execution, allowing server-driven agentic sub-workflows.

---

## Agent Compatibility Assessment

### What it handles natively

- **Structured tool definitions**: JSON Schema for inputs and outputs removes ambiguity about what arguments a tool expects.
- **Machine-readable error signals**: `isError: true` flag in tool results plus JSON-RPC error objects give agents unambiguous failure indicators.
- **Schema and help discoverability**: `tools/list` provides names, descriptions, and schemas on demand; pagination handles large tool sets.
- **Binary and encoding safety**: all binary is base64-encoded in JSON; no raw byte streams reach the agent.
- **No ANSI/color leakage**: responses are typed JSON content, never raw terminal output.
- **Cancellation**: `notifications/cancelled` provides a structured mechanism for the agent or host to cancel in-flight requests.
- **Session management**: stateful sessions with explicit lifecycle (initialize → operate → terminate) prevent accidental state leakage.
- **Authentication and secret handling**: credentials stay at the transport layer (env vars for stdio, OAuth tokens for HTTP) and never appear in tool arguments or results.
- **Progress tracking**: `notifications/progress` lets the host relay long-running operation status without blocking.
- **Streaming partial updates**: SSE-based streaming on Streamable HTTP enables incremental responses for long operations.
- **Platform portability**: transport-agnostic JSON-RPC; SDKs available for TypeScript, Python, C#, Go, Java, Rust, Swift, Ruby, PHP, Kotlin.
- **Idempotency hints**: `idempotentHint` and `readOnlyHint` tool annotations inform the agent whether retrying a call is safe.
- **Destructive operation warnings**: `destructiveHint` annotation signals when a tool may have irreversible effects.
- **Output schema validation**: `outputSchema` provides a formal contract for structured tool output.

### What it handles partially

- **Verbosity and token cost**: tool descriptions and JSON scaffolding always consume context; there is no built-in compression, filtering, or summarization at the protocol level. The server can control output length, but there is no standardized verbosity negotiation between agent and server.
- **Pagination and large output**: list operations are paginated, but individual tool results are returned as a single response. A tool returning a large body of text must handle its own chunking or summarization internally.
- **Timeouts and hanging processes**: the spec recommends timeouts with cancellation notifications, and progress notifications can reset the timeout clock, but enforcement is entirely up to the client implementation. No timeout value is communicated to the server.
- **Retry hints**: `isError: true` signals failure but the protocol does not carry structured retry-after, backoff suggestions, or distinguishing between transient and permanent errors in a machine-actionable way.
- **Race conditions and concurrency**: multiple in-flight requests are supported via JSON-RPC `id` correlation; the spec does not define server-side concurrency guarantees or ordering semantics for tool calls.
- **Undeclared filesystem side effects**: `readOnlyHint` and `openWorldHint` partially describe side-effect scope, but there is no formal contract enumerating all filesystem paths or external systems a tool may touch.
- **Observability and audit trail**: clients SHOULD log tool usage; the protocol provides a structured logging primitive from server to client. However, there is no standard audit log format, centralized trace ID, or correlation across multi-server calls.
- **Prompt injection via output**: tool output is passed to the LLM as content; servers SHOULD sanitize outputs, but there is no protocol-level sanitization or injection detection — the risk is fully delegated to server authors.
- **Schema versioning and output stability**: the MCP protocol versions via date-based spec versions with capability negotiation, but individual tool schemas are unversioned. A tool can change its `inputSchema` or output format without signaling the change to clients.

### What it does not handle

- **Exit codes**: there is no concept of numeric exit codes. Success/failure is conveyed by `isError: true` or JSON-RPC error codes, not by a POSIX-style integer.
- **Stderr vs stdout discipline**: the stdio transport reserves stderr for server logging (optionally captured), but at the protocol level there is no separate stderr channel for tool results. All output comes through the single JSON-RPC response channel.
- **Command composition and piping**: MCP tools are atomic request/response units; there is no built-in pipe or composition model. Chaining tool outputs into another tool's input is the agent's responsibility.
- **Output non-determinism warnings**: no mechanism for a tool to declare that its output is non-deterministic (e.g., random, time-dependent) or to advise the agent accordingly.
- **Argument validation before side effects**: the spec requires servers to validate inputs, and the `inputSchema` enables client-side pre-validation, but there is no standardized two-phase dry-run / confirmation flow at the protocol level (elicitation is the closest, but it is for user input, not argument pre-flight).
- **Child process leakage**: not a protocol concern; fully delegated to server implementation. The protocol has no mechanism to report or prevent orphaned subprocesses.
- **Environment and dependency discovery**: no mechanism for a server to advertise what external dependencies (system tools, credentials, network access) it requires at the environment level.
- **Config file shadowing and precedence**: the protocol does not address configuration file resolution, override ordering, or environment variable precedence at the server level.
- **Working directory sensitivity**: no standard field in tool call or session initialization to communicate or set a working directory. Servers may use roots as a boundary hint, but `cwd` is not a first-class concept.
- **Network proxy unawareness**: no protocol-level mechanism for communicating proxy configuration from client to server. Servers must handle proxy settings independently via environment conventions.
- **Self-update and auto-upgrade behavior**: entirely outside protocol scope. No mechanism to declare or control server auto-upgrade behavior.
- **Signal handling beyond cancellation**: SIGTERM/SIGKILL are mentioned for stdio shutdown, but there is no mechanism for the agent to send arbitrary signals or for servers to declare signal handling capabilities.
- **Idempotency enforcement**: `idempotentHint` is advisory only; there is no protocol-enforced deduplication or at-most-once delivery guarantee.
- **Partial failure and atomicity**: no built-in transaction or rollback semantics. A tool that fails mid-way through a multi-step operation has no standard way to report partial completion or trigger rollback.

---

## Challenge Coverage Table

| # | Challenge | Rating | Reason |
|---|-----------|--------|--------|
| 1 | Exit Codes & Status Signaling | ~ | `isError: true` and JSON-RPC error codes signal failure, but there are no POSIX-style numeric exit codes |
| 2 | Output Format & Parseability | ✓ | Structured JSON with typed content items (`text`, `image`, `resource`) and optional `outputSchema` with JSON Schema validation |
| 3 | Stderr vs Stdout Discipline | ~ | stdio transport separates stderr (logging) from stdout (protocol), but tool results have no stderr channel within the response |
| 4 | Verbosity & Token Cost | ~ | Server controls output content, but no protocol-level verbosity negotiation or filtering; all content is returned in full |
| 5 | Pagination & Large Output | ~ | `tools/list` is paginated; individual tool results are single responses — servers must handle large outputs internally |
| 6 | Command Composition & Piping | ✗ | No built-in pipe or composition primitives; chaining is the agent's responsibility outside the protocol |
| 7 | Output Non-Determinism | ✗ | No annotation or mechanism to declare output is non-deterministic, time-varying, or random |
| 8 | ANSI & Color Code Leakage | ✓ | Responses are typed JSON content, never raw terminal output; ANSI codes cannot appear by design |
| 9 | Binary & Encoding Safety | ✓ | Binary data is base64-encoded in `blob`/`data` JSON fields; no raw binary framing reaches the agent |
| 10 | Interactivity & TTY Requirements | ~ | Elicitation primitive allows server to request user input through the client, but complex interactive TUI workflows are unsupported |
| 11 | Timeouts & Hanging Processes | ~ | Spec recommends per-request timeouts with cancellation notifications; no standard timeout field or server-side enforcement |
| 12 | Idempotency & Safe Retries | ~ | `idempotentHint` and `readOnlyHint` annotations are advisory; no protocol-enforced at-most-once delivery |
| 13 | Partial Failure & Atomicity | ✗ | No transaction, rollback, or partial-completion semantics; tool failure is atomic at the protocol level only |
| 14 | Argument Validation Before Side Effects | ~ | `inputSchema` enables client-side pre-validation; servers MUST validate; no standard two-phase dry-run flow |
| 15 | Race Conditions & Concurrency | ~ | Concurrent requests are correlated via JSON-RPC `id`; no server-side ordering guarantees or concurrency declarations |
| 16 | Signal Handling & Graceful Cancellation | ~ | Structured `notifications/cancelled` for in-flight requests; SIGTERM/SIGKILL for stdio shutdown — no arbitrary signal passing |
| 17 | Child Process Leakage | ✗ | Entirely delegated to server implementation; protocol has no mechanism to report or prevent orphaned processes |
| 18 | Error Message Quality | ✓ | Both protocol errors (JSON-RPC codes + message + data) and tool execution errors (`isError: true` + human-readable content) are structured |
| 19 | Retry Hints in Error Responses | ✗ | No structured retry-after, backoff hints, or transient-vs-permanent error classification in the protocol |
| 20 | Environment & Dependency Discovery | ✗ | No mechanism to advertise required environment variables, system dependencies, or external service requirements |
| 21 | Schema & Help Discoverability | ✓ | `tools/list` returns names, descriptions, and JSON Schema for all tools; paginated; supports `listChanged` notifications |
| 22 | Schema Versioning & Output Stability | ~ | Protocol spec is date-versioned with capability negotiation; individual tool schemas are unversioned and can change silently |
| 23 | Side Effects & Destructive Operations | ~ | `destructiveHint`, `readOnlyHint`, `openWorldHint` annotations provide advisory signals; no formal side-effect contract or enforcement |
| 24 | Authentication & Secret Handling | ✓ | Credentials stay in transport layer (env for stdio, OAuth 2.1 for HTTP); secrets never appear in protocol messages |
| 25 | Prompt Injection via Output | ~ | Servers SHOULD sanitize outputs; protocol carries tool content directly to LLM — no injection detection or sanitization at protocol level |
| 26 | Stateful Commands & Session Management | ✓ | Explicit session lifecycle with `Mcp-Session-Id`; capability negotiation; `notifications/initialized`; graceful termination |
| 27 | Platform & Shell Portability | ✓ | Transport-agnostic JSON-RPC; Tier 1 SDKs for TypeScript, Python, C#, Go; no shell dependency in the protocol |
| 28 | Config File Shadowing & Precedence | ✗ | Protocol does not address configuration file resolution, env var override ordering, or server config precedence |
| 29 | Working Directory Sensitivity | ✗ | No `cwd` field in session init or tool calls; roots primitive provides filesystem boundary hints but not working directory |
| 30 | Undeclared Filesystem Side Effects | ~ | `readOnlyHint` and `openWorldHint` partially scope side effects; no formal listing of filesystem paths a tool may access |
| 31 | Network Proxy Unawareness | ✗ | No protocol-level proxy configuration; servers must handle proxy via environment conventions independently |
| 32 | Self-Update & Auto-Upgrade Behavior | ✗ | Entirely outside protocol scope; no mechanism to declare or control server auto-upgrade |
| 33 | Observability & Audit Trail | ~ | Structured server-to-client logging primitive; clients SHOULD log tool usage; no standard trace ID, correlation format, or centralized audit log |

**Summary**: Native ✓: 10 | Partial ~: 14 | Missing ✗: 9

---

## Strengths for Agent Use

1. **Structured, typed responses**: JSON content with type discriminators eliminates output parsing ambiguity entirely. The agent receives `text`, `image`, `audio`, `resource_link`, or `resource` objects, not raw terminal output.

2. **Explicit error semantics**: two-tier error model (`isError: true` for tool failures, JSON-RPC `error` for protocol failures) gives agents reliable signal without heuristic output parsing.

3. **Self-describing tools**: `tools/list` delivers name, description, and JSON Schema for every tool upfront. The agent knows exactly what arguments each tool expects before calling it.

4. **No ANSI/encoding pollution**: by construction, the protocol cannot carry terminal escape sequences, color codes, or null bytes in text content.

5. **Safe binary transport**: base64 encoding for images, audio, and binary blobs is a first-class design decision, not an afterthought.

6. **Authentication isolation**: secrets live in the transport layer. The agent never sees credentials in tool arguments or outputs, reducing prompt injection attack surface for credentials.

7. **Dynamic capability updates**: `notifications/tools/list_changed` allows the agent to adapt to a changing tool environment without re-initialization.

8. **Cancellation support**: in-flight tool calls can be cancelled via a structured notification, enabling the agent to implement timeouts without killing the server process.

9. **Interactivity bridge**: elicitation lets a server ask the user a question through the agent host mid-tool-execution, covering some interactive use cases without TTY requirements.

10. **Broad SDK ecosystem**: Tier 1 SDKs (TypeScript, Python, C#, Go) with 100% conformance, Tier 2 (Java, Rust), Tier 3 (Swift, Ruby, PHP, Kotlin) — wide language coverage with formal conformance testing.

---

## Weaknesses for Agent Use

1. **No exit code concept**: agents trained on CLI tooling expect numeric status codes. MCP's `isError: true` is semantically equivalent but structurally different; agents must adapt.

2. **Tool result size is unbounded**: a single `tools/call` response can contain an arbitrarily large text body. There is no protocol-level truncation, streaming-of-results, or chunk size negotiation. Large outputs consume agent context in full.

3. **No retry hints**: when a tool fails (`isError: true`), the error content is free-form text. There is no machine-readable field indicating whether the failure is transient, permanent, rate-limited, or requires different arguments.

4. **Tool schemas are unversioned**: a server can change a tool's `inputSchema` or output format between sessions without any protocol-level version signal. Agents may send arguments valid for an old schema.

5. **Annotations are advisory and untrusted**: `idempotentHint`, `destructiveHint`, etc. are informational only. Clients MUST treat them as untrusted unless from a trusted server. An agent cannot rely on them for safety-critical decisions.

6. **No composition primitives**: MCP tools are isolated request/response units. Chaining, piping, or orchestrating multiple tools is the agent's burden. There is no server-declared workflow or dependency graph.

7. **Prompt injection risk via tool output**: unstructured text in tool result content flows directly into the LLM context. A malicious or compromised server can embed instruction-following text that hijacks agent behavior. The protocol provides no defense.

8. **No working directory context**: agents that operate on files need to know the relevant working directory, but MCP has no `cwd` field. Roots provide boundaries but not a specific working path.

9. **Progress notifications are not streaming results**: progress reports describe completion percentage, not partial output. An agent cannot process the beginning of a large result before the end is ready.

10. **stdio transport is local only**: for remote servers, Streamable HTTP is required, introducing OAuth complexity, DNS rebinding attack surface, and network latency. The security spec for HTTP is substantial.

---

## MCP vs CLI: When to Use Which

| Concern | MCP | CLI |
|---------|-----|-----|
| Output format | Structured JSON, typed content items | Raw text; requires parsing conventions |
| Error signaling | `isError: true` + JSON-RPC error codes | Exit code (0/non-zero) + stderr |
| Schema discoverability | Built-in via `tools/list` + JSON Schema | `--help` text; no machine-readable standard |
| Binary data | Base64 in JSON | Raw bytes on stdout or file paths |
| Authentication | OAuth 2.1 (HTTP) or env vars (stdio) | env vars, config files, secret stores |
| Streaming results | Progress notifications; SSE on HTTP | Stdout line-by-line as process runs |
| Session state | Explicit, negotiated, lifecycle-managed | Implicit via filesystem or env vars |
| Interactivity | Elicitation primitive | Full TTY, stdin prompts |
| Cancellation | `notifications/cancelled` | SIGINT/SIGTERM |
| Composition | Agent-side only | Shell pipes, subshells, xargs |
| Existing tool coverage | Growing but curated ecosystem | Every CLI tool ever written |
| Deployment complexity | Server process + SDK + protocol setup | Binary + PATH |
| Verbosity control | Server-determined; no negotiation | Flags (`-q`, `-v`, `--format`) |
| Retry hints | None in protocol | Exit codes + stderr patterns |
| Working directory | Not in protocol | Process `cwd` inheritance |

**Use MCP when**: building a new integration from scratch, need structured output guarantees, need auth integration, need the tool to be usable by multiple AI clients, want to expose binary or multi-modal data, or need session state across multiple calls.

**Use CLI when**: the tool already exists as a well-behaved CLI, you need shell composition, you need working directory semantics, you need compatibility with non-AI tooling, you need fine-grained verbosity flags, or deployment simplicity outweighs protocol overhead.

**Use both**: wrap an existing CLI in an MCP server to get structured output, schema discovery, and auth integration while preserving the underlying implementation. This is the most common pattern for integrating legacy tooling.

---

## Verdict

MCP is a well-engineered protocol that solves the hardest problems for agent-tool integration: it eliminates output ambiguity by making all responses structured JSON, provides explicit and machine-readable error semantics, delivers self-describing tool schemas upfront, and isolates authentication from the agent's context. For the 33 challenges evaluated, MCP natively resolves 10 (output format, ANSI pollution, binary safety, schema discoverability, authentication, session management, platform portability, error quality, cancellation, and structured tool definitions), partially addresses 14 more through annotations, progress notifications, pagination, and elicitation, and leaves 9 genuinely unaddressed — most critically: retry hints, working directory context, composition primitives, child process management, and prompt injection defense. The protocol's biggest remaining gap relative to CLI usage is not in what it broke but in what it has not yet formalized: tool schema versioning, output size bounds, and machine-actionable retry guidance. For greenfield agent tooling, MCP is the right default. For legacy CLI integration, the practical path is to wrap existing CLIs in thin MCP servers that translate exit codes to `isError`, strip ANSI, and add JSON Schema declarations — gaining all of MCP's agent ergonomics without rewriting working tools.
