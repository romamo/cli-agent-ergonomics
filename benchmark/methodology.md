# Benchmark Methodology

## What is being measured

The benchmark measures **agent overhead** — the extra tokens, time, and API calls an AI agent spends when a CLI tool does not conform to the CLI Agent Ergonomics spec. The delta between `cli-bad` and `cli-good` on each scenario is the concrete cost the spec eliminates.

## Experimental design

### Controlled variables
- **Model**: Claude claude-sonnet-4-6 (fixed version)
- **System prompt**: identical for both CLI modes (no CLI-specific coaching)
- **Task**: identical natural-language task description
- **Underlying data**: identical (same records, same responses, same errors)
- **Temperature**: 0 (deterministic)

### Variable
- **CLI compliance**: `bad` (default behavior) vs `good` (spec-compliant)

### Mock CLI design

Both CLIs are shell scripts in `harness/cli/bad/` and `harness/cli/good/`. They return pre-defined responses — no network calls, no real state changes. This ensures reproducibility and isolates the spec's effect from real-world variance.

`cli-bad` deliberately implements common anti-patterns:
- Plain text output mixed with ANSI color codes
- `exit 1` for all errors (no semantic exit codes)
- No pagination — dumps all records at once
- Interactive prompts on destructive operations (which deadlock without TTY)
- No `--output json` flag
- Help text on stdout, not stderr

`cli-good` implements the spec:
- `ResponseEnvelope` JSON on every response
- 14-code exit table with `retryable` and `side_effects`
- Paginated list responses with `page.next_cursor`
- `--dry-run`, `--yes`, `--output`, `--limit`, `--idempotency-key`
- `manifest` subcommand returning full command tree

### Metrics

| Metric | How collected | What it measures |
|--------|--------------|-----------------|
| `total_tokens` | `sum(usage.input_tokens + usage.output_tokens)` per call | Total API cost |
| `input_tokens` | `sum(usage.input_tokens)` per call | Context window pressure |
| `output_tokens` | `sum(usage.output_tokens)` per call | Generation cost |
| `api_calls` | Count of `messages.create` calls | Round-trip count (latency multiplier) |
| `time_ms` | `time.perf_counter()` wall clock | End-to-end latency |
| `success` | Agent answer matches expected output | Correctness |
| `steps` | Count of tool use blocks | How much exploration was needed |

### Agent loop

```
1. Send task + tool definition to Claude
2. If response contains tool_use blocks:
   a. Execute each tool call against the CLI scripts
   b. Append assistant message + tool results to conversation
   c. Go to 1
3. If response is end_turn: record final answer, stop
4. If steps > MAX_STEPS (20): record failure, stop
```

The agent has no knowledge of which CLI mode it is using. It receives the same system prompt in both conditions.

## Threat model

**What this benchmark does not control for:**
- Real network latency (CLIs are mocked)
- Model version drift (pin the model ID)
- Non-determinism at temperature > 0 (use temperature=0)
- Prompt sensitivity (run 3× per scenario, take median)

**Interpretation caution:**
- A higher token count for `cli-bad` reflects the agent parsing unstructured output, retrying on bad exit codes, and recovering from hangs — not just verbosity
- `input_tokens` growth across steps reflects context accumulation; unbounded output from `cli-bad` is the main driver
- `api_calls` delta directly measures retry loops and discovery overhead

## Reproducibility

Results files in `results/` include:
- `model`: exact model ID used
- `date`: ISO date
- `anthropic_sdk_version`: SDK version
- `scenario_hash`: SHA256 of the scenario + CLI scripts (detects drift)

Re-run with the same scenario hash to compare across model versions.
