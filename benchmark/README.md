# CLI Agent Ergonomics — Benchmark

Measures the real cost of non-compliant CLI tools on AI agent performance: **time**, **token spend**, and **context window usage**.

Each scenario runs an AI agent (Claude) against two CLI implementations of identical functionality:
- **`cli-bad`** — default behavior: plain text output, ANSI colors, inconsistent exit codes, no pagination, no schema
- **`cli-good`** — spec-compliant: JSON envelopes, typed exit codes, pagination, manifest, structured errors

The delta between the two is the overhead the spec eliminates.

---

## Results

> Run `python harness/run.py --all` to populate this table.

| Scenario | Metric | cli-bad | cli-good | Delta |
|----------|--------|---------|----------|-------|
| List & extract | Total tokens | — | — | — |
| List & extract | Time (ms) | — | — | — |
| List & extract | API calls | — | — | — |
| Retry safety | Total tokens | — | — | — |
| Retry safety | Time (ms) | — | — | — |
| Retry safety | API calls | — | — | — |
| Discovery | Total tokens | — | — | — |
| Discovery | Time (ms) | — | — | — |
| Discovery | API calls | — | — | — |
| Error diagnosis | Total tokens | — | — | — |
| Error diagnosis | Time (ms) | — | — | — |
| Error diagnosis | API calls | — | — | — |
| Destructive ops | Total tokens | — | — | — |
| Destructive ops | Time (ms) | — | — | — |
| Destructive ops | API calls | — | — | — |

---

## Scenarios

| ID | Name | Primary challenge cluster | Key spec requirements |
|----|------|--------------------------|----------------------|
| [S1](scenarios/s1-list-extract.md) | List & extract IDs | Pagination, context overflow | F-018, F-019, F-052, O-003 |
| [S2](scenarios/s2-retry-safety.md) | Deploy with conflict | Exit codes, retry safety | F-001, F-002, C-013, C-014 |
| [S3](scenarios/s3-discovery.md) | Discover command surface | Schema, manifest, token spend | C-015, O-013, O-041 |
| [S4](scenarios/s4-error-diagnosis.md) | Diagnose a failure | Error quality, structured errors | C-013, F-037, F-063 |
| [S5](scenarios/s5-destructive-ops.md) | Bulk delete with dry-run | Destructive ops, partial failure | C-002, C-004, C-008, C-009 |

---

## Running the benchmark

```bash
cd benchmark/harness
pip install anthropic
export ANTHROPIC_API_KEY=...

# Run all scenarios, both CLIs
python run.py --all

# Run one scenario
python run.py --scenario s1 --mode bad
python run.py --scenario s1 --mode good

# Output results JSON
python run.py --all --output ../results/$(date +%Y%m%d).json
```

Results are saved as JSON in `results/` and printed as a summary table.

---

## How it works

1. The harness starts an agent loop using the Claude API with tool use
2. The agent is given the scenario task and a single tool: `run_cli(command, args)`
3. The tool executes `cli/bad/<command>` or `cli/good/<command>` (shell scripts returning mock data)
4. The loop runs until the agent produces a final answer or hits the step limit
5. At the end, `usage.input_tokens` and `usage.output_tokens` are summed across all API calls

Metrics collected per run:
- `total_tokens` — input + output tokens across the full agentic loop
- `input_tokens` — context consumed (proxy for context window pressure)
- `output_tokens` — generation cost
- `api_calls` — number of model invocations (each tool call = one roundtrip)
- `time_ms` — wall-clock time
- `success` — did the agent produce the correct answer?
- `steps` — number of tool calls made

See [`methodology.md`](methodology.md) for scoring details and threat model.
