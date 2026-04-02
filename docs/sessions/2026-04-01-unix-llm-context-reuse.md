# Unix LLM Context Reuse in Agent-Facing CLI Design

**Date:** 2026-04-01  
**Topic:** How CLI developers can exploit LLM training on Unix commands — and what assumptions agents silently make  
**Spec changes:** 12 new requirements (REQ-F-068–078, REQ-C-028), 1 amendment (REQ-F-043), spec v1.5 → v1.6

---

## Key Insights

### 1. Unix conventions are a semantic compression channel
LLM training on Unix tools encodes behavioral expectations into short names and flag patterns. A CLI developer who aligns naming and structure with Unix conventions transfers that compressed knowledge directly into agent zero-shot accuracy — without documentation. The agent arrives with correct priors about side effects, retry safety, and argument shapes.

### 2. The design rule: inherit vocabulary, override mechanics
Unix *naming and semantics* should be preserved. Unix *output format, exit code precision, glob contracts, and interactivity* should be replaced with agent-safe equivalents. The failure modes catalogued in the spec (§1, §51, §57, §63…) are all Unix mechanics that need overriding — not reasons to abandon Unix naming entirely.

### 3. Different training corpora activate different mental models
Each corpus (kubectl, AWS CLI, curl, terraform, git, docker-compose) is densely trained and activates a specific interaction protocol. The design question is: which corpus does your tool most resemble? Match that corpus's conventions to activate the densest available prior. A deployment tool should look like terraform. A resource manager should look like kubectl. A transfer tool should look like curl.

### 4. Three layers of agent-facing CLI design
- **Naming layer** — Unix vocabulary, verb-noun grammar, synonym support activate correct priors
- **Mechanics layer** — structured output, precise exit codes, isatty detection, signal handling make behavior predictable
- **Runtime self-documentation layer** — `--explain`, `--help --format json`, `__complete`, deprecation warnings, `next_steps` in errors reduce the agent's epistemic load at runtime

### 5. Silent assumptions are the hardest failure class
Agents never state their assumptions. `--help` purity, `SIGPIPE` handling, `$HOME` isolation, first-run init behavior, `O_CLOEXEC` on subprocesses — these are all violated silently and produce failures that look like something else entirely. They are the hardest bugs to diagnose in agent-CLI integration and were entirely absent from the spec before this session.

### 6. Positive design vocabulary was missing from the spec
The spec catalogued failure modes to defend against. It had no guidance on which Unix conventions to *preserve* because they carry correct trained priors. This session identified the gap and documented it — the spec now has both the failure catalogue and the positive design vocabulary.

### 7. Spec gaps were requirements, not challenges
The 17 identified gaps were all implementation contracts (what the tool must do), not new failure mode descriptions (what goes wrong). The underlying problems were already covered by existing challenges. What was missing was the corresponding requirements making the solutions explicit and enforceable. 12 new requirements + 1 amendment close all high-impact gaps.

---

## Part 1 — Why Unix-Style Interfaces Fail Agents

Unix command design was optimized for human typists at a terminal in the 1970s. Re-using that interface in agent-facing CLIs imports those constraints into a context where they cause active harm.

| Unix convention | Why it made sense then | Why it fails agents |
|---|---|---|
| Short flags `-f -r` | Minimize keystrokes | Ambiguous across tools, drives hallucination |
| Positional args | Natural language feel | Order-sensitive, no schema representation |
| Silent success | Reduce noise for humans | Agents need structured confirmation |
| Non-error non-zero | Expressiveness | Corrupts retry logic |
| Shell glob contract | Shell handles it | Bypassed under subprocess invocation |
| Locale-aware output | Human readability | Breaks deterministic parsing |
| Combined flags | Typing convenience | No machine-readable representation |
| Loose stderr | Informational | No stable signal/noise boundary |

**Spec coverage:** §35 (hallucination), §69 (arg order), §2 (output format), §1 (exit codes), §51 (glob), §57 (locale), §21 (schema), §3 (stderr)

---

## Part 2 — How to Reuse LLM Unix Knowledge as a Design Asset

The principle: **preserve Unix naming and semantics, override the broken mechanics.**

### 2.1 Naming and Vocabulary

- **Name commands after Unix analogues** — `list`, `get`, `put`, `remove`, `exec`, `watch`, `stat`, `diff`, `apply` carry pre-trained behavioral expectations
- **Verb-noun subcommand grammar** — `tool resource create`, `tool resource list` mirrors `git commit`, `kubectl get pods`; agent infers side-effect profile from verb
- **Verb synonyms** — support `rm`/`remove`/`delete`, `ls`/`list`, `cp`/`copy`; first guess is correct regardless of which synonym the agent picks
- **`apply` as idempotent upsert** — deeply trained from `kubectl apply`; agent treats it as create-if-absent, update-if-present, retry-safe
- **`up`/`down` as composition lifecycle** — trained from docker-compose, vagrant, terraform; implies dependency resolution and completeness
- **`start`/`stop`/`restart`/`reload`/`status`** — trained from systemctl, supervisorctl; agents manage long-running processes with these five verbs
- **`install`/`uninstall`/`upgrade`/`outdated`** — trained from apt, brew, npm, pip; agents know `install` is idempotent, `upgrade` changes versions
- **`init`/`status`/`version`** — universal entry points agents try first in any unknown environment
- **`exec` subcommand** — trained from `docker exec`, `kubectl exec`; run command inside a resource's context
- **`logs` subcommand** — trained from `docker logs`, `kubectl logs`; accepts `--since`, `--tail`, `--follow`
- **`describe`/`inspect`** — trained from `kubectl describe`, `docker inspect`; returns full resource detail
- **`--validate`/`--check`** — trained from `nginx -t`, `terraform validate`; zero-side-effect preflight

### 2.2 Flag Conventions

- **`--dry-run`/`-n`** — agents will use it before mutating; trained from rsync, ansible, make
- **`--verbose`/`-v`** — escalate to `-vv`/`-vvv` for more diagnostic signal; trained from ssh, curl, ansible
- **`--output`/`--format json`** — highest-leverage single flag; trained from `aws --output json`, `kubectl -o json`, `gh --json`
- **`--force`/`-f`** — skip confirmation; agents know this and will use it when appropriate
- **`--recursive`/`-r`** — traverse depth; expected with depth-limiting `--max-depth`
- **`--quiet`/`-q`** — suppress non-essential output; agents use in batch contexts
- **`--all`/`-a`** — include hidden/all items
- **`--no-*` negation pattern** — `--no-color`, `--no-pager`, `--no-interactive`; agents try negation of known flags
- **`--timeout` with duration suffixes** — `30s`, `5m`, `1h`; trained from curl, kubectl
- **`--color=auto|always|never`** — three-value enum; agents pass `--color=never` in pipelines
- **`--since`/`--until`/`--limit`** — time-bounded queries; trained from journalctl, docker logs, git log
- **`--follow`/`-f`** — live-stream signal; trained from tail -f, kubectl logs -f
- **`--watch`** — stream updates until killed; trained from kubectl --watch, webpack --watch
- **`--wait`/`--no-wait`** — synchronous vs async invocation choice; trained from kubectl wait
- **`--fields`/`--columns`** — output narrowing; trained from cut, awk, kubectl custom-columns
- **`--query` with jq/JMESPath** — agents write expressions correctly first try; trained from aws --query, kubectl jsonpath
- **`--jq <expression>`** — embed jq filter directly; agents are fluent in jq syntax
- **`--label`/`-l key=value`** — resource filtering by metadata; trained from kubectl -l
- **`--namespace`/`-n`** — scope isolation for parallel agent invocations; trained from kubectl -n
- **`--set key=value`** — inline config override; trained from helm --set
- **`--var key=value`/`--var-file path`** — variable injection; trained from terraform -var, ansible -e
- **`--tags`/`--skip-tags`** — selective execution; trained from ansible --tags, pytest -m
- **`--on-error fail|continue|rollback`** — error handling strategy; trained from make -k, helm --atomic
- **`--parallel`/`-j`** — concurrency control; trained from make -j, xargs -P
- **`--from-file`/`--from-literal`/`--from-env-file`** — multiple input source modes; trained from kubectl create secret
- **`--for=condition`** — bounded waiting; trained from kubectl wait --for=condition=Ready
- **`-e KEY=VALUE`** — runtime context injection; trained from docker run -e
- **`-e`/`--expression`** — inline transformation; trained from sed -e, awk -e, perl -e
- **`--diff`** — show what would change; trained from git diff, terraform plan
- **`--as`** — impersonation for permission probing; trained from kubectl --as
- **`--generate-skeleton`/`--input-file`** — two-step protocol for complex inputs; trained from aws --generate-cli-skeleton
- **`--no-paginate`/`--page-size`/`--starting-token`** — pagination trio; trained from AWS CLI
- **`--idempotency-key`/`--request-id`** — safe retry deduplication; trained from AWS SDK, Stripe
- **`--continue`/`--resume`** — resume interrupted operations; trained from wget --continue, rsync --partial
- **`--checkpoint-file`/`--batch-size`** — resumable data pipelines; trained from wget, Spark
- **`--ttl`/`--expires-at`** — time-bounded resources; trained from Redis EXPIRE, kubectl TTL controllers
- **`--workspace`** — named isolation context; trained from terraform workspace, npm workspaces
- **`--plan-file`** — save and replay execution plans; trained from terraform plan -out
- **`--assert`/`--expect`** — inline verification; trained from curl --fail, test frameworks
- **`--update-golden`** — snapshot testing; trained from Jest --updateSnapshot
- **`--porcelain`** — explicit stability contract; trained from git status --porcelain
- **`--idempotency-key`** — retry-safe mutation deduplication

### 2.3 Output Conventions

- **`--format json` is the machine contract** — enables all downstream agent parsing
- **One-item-per-line** — safe for xargs, shell loops; trained from find, ls -1, grep
- **TSV over CSV** — no quoting rules, safe for cut/awk; trained from cut, paste, sort
- **`KEY=VALUE` per line** — parseable without libraries; trained from env, printenv
- **`---` document separator** — multi-document YAML stream; trained from kubectl get -o yaml
- **JSON Lines (JSONL)** — one JSON object per line; streaming-safe; trained from docker events, kubectl --watch
- **`-print0`/`--null`/`-0`** — null-terminated for safe bulk piping; trained from find -print0 | xargs -0
- **`--no-headers`** — strip header row for column parsing; trained from kubectl --no-headers, ps
- **Verb output contracts** — `create` returns ID, `get` returns full resource, `list` returns array, `delete` returns confirmation
- **`--porcelain`** — frozen, versioned, stable format; a stability promise not just a format choice
- **Output field stability tiers** — stable fields in `data`, experimental in `_experimental`
- **Schema version field** — `{"schema_version": "1", ...}` in all JSON output

### 2.4 Environment Variables

- **`NO_COLOR=1`** — disable ANSI output; universal standard
- **`CI=true`** — headless mode; disables prompts, spinners, color, interactive behavior
- **`DEBUG=tool`/`TOOL_DEBUG=1`** — verbose tracing
- **`TOOL_TOKEN`/`TOOL_API_KEY`** — credential injection
- **`TOOL_CONFIG`** — override config file path
- **`HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`** — network proxy; agents expect tools to respect these
- **`$XDG_CONFIG_HOME`/`$XDG_DATA_HOME`/`$XDG_CACHE_HOME`** — base directory overrides; agents use for isolation
- **`PAGER=cat`** — agents set this; tools must respect it

### 2.5 Config File Locations

Agents look for config in predictable places before asking:
- `~/.toolrc`
- `~/.config/tool/config.yaml` (XDG)
- `./.tool.yaml` (project-local)
- `/etc/tool/config.yaml` (system-wide)

**Strict precedence:** flag > env var > config file > default

### 2.6 Input Conventions

- **`-` for stdin** — trained from cat, diff, patch, jq; agents use when tool requires a file path
- **`/dev/stdin` as file path** — escape hatch when tool doesn't support `-`; fails if tool stats before opening
- **`--` end-of-flags** — trained from every shell script; agents use when passing user-controlled strings
- **Heredoc-safe stdin** — tools accepting multi-line stdin work with agent-generated heredocs

### 2.7 Streaming and Async Protocols

- **`--follow`/`-f`** — open-ended event consumption; agent launches and reads each line as an event
- **`--watch`** — stream updates; agent reads each line as a state change
- **`--events`** — chronological event stream; richer than --follow, includes history
- **`--for=condition`** — declare what you're waiting for; tool blocks until condition met
- **JSONL for streaming** — one JSON per line; each independently parseable without buffering

### 2.8 Documentation and Discovery

- **Man page format** — SYNOPSIS/OPTIONS/EXAMPLES/EXIT STATUS/ENVIRONMENT/SEE ALSO; parsed with high fidelity by agents
- **SYNOPSIS as formal grammar** — `<required>`, `[optional]`, `(a|b)`, `...`, `TYPE`; agents extract call signature from SYNOPSIS alone
- **`EXAMPLES` section** — highest-leverage documentation investment; each example is a training instance
- **Flag type annotations** — `STRING`, `INT`, `ENUM`, `FILE`, `DURATION`; agents enforce types pre-call
- **`SEE ALSO`** — agents follow cross-references to find related commands
- **`completion` subcommand** — signals well-structured command tree; agents use `tool __complete` for valid value discovery
- **`--explain`** — trained from `kubectl explain`; agents query field schemas at runtime
- **`--help --format json`** — machine-readable help; turns --help into a schema API
- **`--generate-skeleton`** — template for complex inputs; agents populate and pass via --input-file
- **`tool capabilities`/`tool features`** — runtime capability advertisement; agents orient in unknown environments
- **"Did you mean?"** — structured suggestion on stderr; agents self-correct on next attempt
- **Structured deprecation warnings** — `DEPRECATED: use X instead`; agents self-migrate
- **`--version` outputs just semver** — `tool 1.2.3`; parseable with `cut`
- **`tool states`/`tool transitions`** — state machine visibility; agents plan lifecycle operations

### 2.9 Corpus-Specific Patterns

Each training corpus activates a specific mental model:

| Corpus | Key patterns | What the agent inherits |
|--------|-------------|------------------------|
| `curl` | `-X METHOD`, `-H header`, `-d data`, `-u user:pass`, `--fail`, `--retry` | Complete HTTP interface vocabulary |
| `kubectl` | `-n namespace`, `-l selector`, `-o json`, `apply`, `wait --for`, `explain` | Multi-tenant resource management |
| `git` | `HEAD~N`, `--porcelain`, `--patch`, ref syntax | Version-addressing and stable output |
| `terraform` | `plan`/`apply`/`destroy`, `--var`, `--plan-file`, workspaces | Two-phase preview + execute |
| `ansible` | `--tags`, `--limit`, `--check`, `--diff`, `--extra-vars` | Selective idempotent execution |
| `helm` | `--set`, `--values`, `--atomic`, `--dry-run` | Parameterized declarative deployment |
| `docker` | `exec`, `logs --follow`, `-e KEY=VALUE`, `--rm` | Container lifecycle |
| `docker-compose` | `up -d`, `down -v`, `logs -f` | Multi-service orchestration |
| `AWS CLI` | `--output json`, `--query`, `--no-paginate`, `--page-size` | Paginated cloud resource management |
| `make` | `install`, `test`, `clean`, `build` targets | Universal project entry points |
| `jq` | Filter syntax, `-r`, `-c`, `--arg` | JSON transformation language |

**Design question:** Which corpus does your tool most resemble? Match that corpus's conventions to activate the densest available prior.

### 2.10 Interaction Protocols

Full multi-step workflows agents already know end-to-end:

| Protocol | Trained from | Agent behavior |
|----------|-------------|----------------|
| Null-pipe | `find \| xargs -0` | Safe bulk composition |
| Follow-stream | `tail -f`, `kubectl logs -f` | Open-ended event consumption |
| Exec-in-context | `docker exec` | Commands inside environments |
| Label selector | `kubectl -l` | Set-based resource filtering |
| Diff-then-apply | `git diff` + `apply` | Two-phase change verification |
| `--dry-run` → `--apply` | ansible, rsync, terraform | Preview before commit |
| `--wait --for=condition` | `kubectl wait` | Bounded async waiting |
| `describe` then act | `kubectl describe` | Full state before mutation |
| `init` then use | `git init`, `npm init` | Bootstrap before operation |

---

## Part 3 — Silent Assumptions Agents Make

Things agents assume are already true without checking.

### 3.1 Ambient Unix Environment

- **`jq` is installed** — agents pipe to jq constantly; it is not always present
- **`date` behaves like GNU date** — macOS ships BSD date with different flags; `-d '1 hour ago'` fails silently
- **`bash` is at `/bin/bash`** — not true on NixOS, some containers, or systems using dash as /bin/sh
- **Common utilities in `$PATH`** — grep, awk, sed, sort, cut, wc, head, tail, tr; not guaranteed in minimal containers
- **`sudo` works as expected** — agents prepend sudo when needed; also know `sudo -E` preserves env and `SUDO_USER` identifies original caller
- **`$HOME`, `$USER`, `$PATH`, `$SHELL`, `$PWD` are set** — not guaranteed in all exec contexts
- **`/tmp` is writable** — not true in some containers or restricted environments
- **`/dev/null`, `/dev/stdin`, `/dev/stdout`** exist — agents use these as file paths

### 3.2 Tool Behavior Assumptions

- **`--help` has no side effects** — agents call it freely for discovery and introspection
- **`--version` has no side effects** — agents call it to check compatibility
- **Non-mutating commands (get, list, status) are truly read-only** — agents retry them freely and in parallel
- **The same command called twice produces the same output** — determinism assumed for reads
- **Tools do not change the working directory** — relative paths stay valid across calls
- **Tools do not exit 0 and produce no output** — empty success must be structured
- **First-run and Nth-run behavior are identical** — no silent initialization on first call
- **Subcommands only accumulate across versions** — removals break cached agent mental models
- **Binary name matches tool name** — `git` is `git`, not `git-2.39`

### 3.3 Environment Isolation Assumptions

- **`$HOME` isolation works** — changing `$HOME` redirects all `~/` paths; tools must resolve at call time, not import time
- **XDG base directories are respected** — `$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`, `$XDG_CACHE_HOME`
- **`$TERM=dumb` suppresses all formatting** — independent of `isatty()` and `NO_COLOR`; all three signals must independently suppress formatting
- **`CI=true` suppresses interactive behavior** — agents running in CI-like contexts set this; tools must honor it
- **`.env` file loading works** — agents place `.env` in CWD for per-invocation config; tools that auto-load honor this isolation primitive

### 3.4 Process and System Assumptions

- **`SIGPIPE` exits gracefully** — agents pipe output to head/grep; SIGPIPE default handler exits 141 (looks like failure)
- **`SIGINT` exits 130** — agents send Ctrl+C to cancel; expect 130, not 1
- **`SIGTERM` triggers cleanup** — agents send SIGTERM to stop; tools must release locks and clean temp files
- **`PIPESTATUS` captures all pipeline exit codes** — agents in strict scripts check every stage; tools in middle of pipe must exit non-zero if they fail
- **`set -o pipefail` is safe** — agents write scripts with pipefail; non-error non-zero exits break this
- **`&&` chaining works** — every command exits 0 on success and non-zero on any failure, no exceptions
- **File descriptors don't leak** — tools that exec subprocesses must use `O_CLOEXEC`; leaked fds cause EOF hangs
- **Child processes are cleaned up** — no zombie processes after tool exits
- **Temp files are cleaned up** — no litter in CWD or `/tmp` after normal or abnormal exit

### 3.5 Output and Parsing Assumptions

- **Stdout is clean on non-zero exit** — agents parse stdout only when exit is 0; partial output + non-zero exit = corrupt parse
- **stdout is flushed before exit** — Python, Java, Go may buffer; abnormal exit loses last lines
- **Line endings are LF, not CRLF** — `\r` in output breaks string comparisons and field parsing
- **Timestamps include timezone** — `2026-04-01T12:00:00` is ambiguous; always include `Z` or `+HH:MM`
- **Output encoding is UTF-8** — regardless of `$LANG` or `$LC_ALL`
- **Error messages are in English** — agent error parsing is trained on English; localized messages produce hallucinated interpretations
- **No stack traces on stderr** — Python/Java tracebacks look like multiple error events; catch at top level

### 3.6 Pagination Assumption

- **List commands return all results** — agents assume they received everything; a command that silently returns only the first page causes decisions on incomplete data
- **`has_more: false` on the last page** — must be explicit even when obviously last

---

## Part 4 — Implementation Requirements

What to actually build into your CLI tool.

### 4.1 Critical Runtime Contracts

| Requirement | Implementation |
|-------------|---------------|
| `--help` is pure | Exit before any initialization code runs |
| Stdout clean on error | On non-zero exit: nothing to stdout, only stderr |
| `SIGPIPE` handled | Catch SIGPIPE, exit 0 (or known code) |
| Atomic writes | Write to tmpfile in same directory, then `rename()` |
| `isatty(stdin)` auto-detects non-interactive | Suppress all prompts when stdin is not a TTY |
| Deterministic output ordering | Always sort list output by a stable key |
| Read commands provably side-effect free | Audit every get/list/status for hidden writes |
| `$HOME` resolved at call time | Not at import/module load time |
| Lock files cleaned on all exit paths | `try/finally` covering SIGTERM, exceptions, normal exit |
| Child processes reaped before exit | Use process groups; wait for all children |

### 4.2 Semantic Contracts

| Requirement | Implementation |
|-------------|---------------|
| Unknown flags are errors | Exit non-zero, name the unrecognized flag |
| Zero results exits 0 | Empty collection = success, not error |
| `null`/absent/empty string are distinct | Pick a convention, hold it across all fields |
| `ALREADY_EXISTS` returns existing resource | Structured error with resource in body |
| Delete is idempotent | `NOT_FOUND` exits 0 |
| No stack traces on stderr | Top-level exception handler emits one structured error |
| Validation before side effects | All argument errors before any external state change |
| `TOOL_` prefix on all env vars | Except `NO_COLOR`, `CI`, `HOME`, `XDG_*` |
| Schema version in all JSON output | `{"schema_version": "1", ...}` |
| Structured output even when empty | `{"items": [], "total": 0}` not silence |

### 4.3 Environmental Hygiene

| Requirement | Implementation |
|-------------|---------------|
| Secrets never in argv | Accept via env var, `--token-file`, or stdin |
| Implicit pagination must signal | Include `next_token` and `has_more` in every paginated response |
| Telemetry never blocks | Fire-and-forget async; failure must not affect exit code or output |
| Fast startup | Lazy-load everything; defer all I/O until command needs it |
| Line endings are LF | Force `\n` regardless of platform |
| Timestamps include timezone | ISO 8601 with `Z` or `+HH:MM` always |
| Errors in English | `LC_ALL=C` for error message generation |
| File descriptors don't leak | `O_CLOEXEC` on all opens; `close_fds=True` in subprocess calls |
| Internal retries are visible | Expose `--retries`/`--retry-delay` or include retry count in output |
| `$HOME` and XDG honored | Resolve at call time; never cache home directory at startup |
| `$TERM=dumb` + `NO_COLOR` + `!isatty()` | All three independently suppress formatting |
| Temp files have restrictive permissions | `600` not `644`; use `mktemp` |
| CWD never changes | Never call `chdir()` without restoring afterward |
| First-run init is explicit or infallible | `tool init` subcommand, or silent and guaranteed to succeed |

---

## Part 5 — The Core Design Principle

> **Inherit Unix vocabulary and semantics. Replace Unix output format, exit code precision, interactivity, and glob contracts with agent-safe equivalents.**

The LLM's Unix training is a compression artifact — it encodes a huge amount of behavioral expectation into short names and flag conventions. A CLI developer who aligns naming and structure with Unix conventions transfers that compressed knowledge directly into agent zero-shot accuracy, while the spec's requirements handle the mechanics that Unix got wrong for this context.

**The goal is not to look like a Unix tool. It is to activate the right mental model in the agent. Unix naming is the activation key.**

At the highest level, the ideal agent-facing CLI is not just machine-readable — it is **machine-reasoned-about**: designed to reduce the agent's epistemic load at every interaction point.

| Layer | What it gives the agent |
|-------|------------------------|
| Unix naming conventions | Correct behavioral priors without docs |
| Runtime self-documentation | Schema, valid values, deprecation hints |
| Temporal contracts | Resumability, idempotency, expiration |
| Environmental hygiene | Isolation, parallelism, no hidden state |

---

## Part 6 — Spec Gaps Identified

Concepts discussed in this session not yet represented in the spec:

1. **Positive Unix convention layer** — a curated list of conventions worth *inheriting* (currently only failure modes to defend against)
2. **Silent assumption catalogue** — `--help` purity, `SIGPIPE`, `$HOME` isolation, XDG, CWD stability, first-run init (none documented)
3. **Training corpus alignment guide** — which corpus to model against for which tool type (kubectl, AWS CLI, curl, git, make)
4. **Environmental hygiene checklist** — secrets in argv, telemetry, startup latency, CRLF, timezone, English errors, fd leaks
5. **Implicit pagination** as a named failure mode (related to §43 output size, but distinct)
6. **Schema version field** as a requirement (related to §22 versioning, but more specific)
7. **`ALREADY_EXISTS` / idempotent create pattern** as a named requirement
