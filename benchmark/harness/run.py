from __future__ import annotations

"""
CLI Agent Spec Benchmark Harness

Measures token spend, time, and API call count for an AI agent completing
tasks against a non-compliant CLI (cli-bad) vs a spec-compliant CLI (cli-good).

Usage:
    python run.py --all
    python run.py --scenario s1 --mode bad
    python run.py --scenario s1 --mode good
    python run.py --all --output ../results/$(date +%Y%m%d).json
"""

import argparse
import json
import os
import subprocess
import sys
import time
import hashlib
from pathlib import Path
from typing import Any

import anthropic

ROOT = Path(__file__).parent
CLI_DIR = ROOT / "cli"
SCENARIOS_DIR = ROOT.parent / "scenarios"

def check_success(scenario: dict, final_answer: str) -> bool:
    """Check if the final answer satisfies the scenario's success criteria."""
    answer = final_answer.lower()
    expected = scenario["expected"]
    if isinstance(expected, list):
        # All items must appear in the answer
        return all(e.lower() in answer for e in expected)
    return expected.lower() in answer


SCENARIOS = {
    "s1": {
        "file": "s1-list-extract.md",
        "task": (
            "List ALL deployments and return their IDs. "
            "There are multiple pages — make sure you retrieve every single one."
        ),
        # All 20 IDs must appear; spot-check first, middle, and last pages
        "expected": ["deploy-001", "deploy-010", "deploy-015", "deploy-019", "deploy-020"],
    },
    "s2": {
        "file": "s2-retry-safety.md",
        "task": (
            "Deploy version 2.1.0 of the app to staging. "
            "If it fails, retry until it succeeds or you are sure it cannot."
        ),
        "expected": "deployed",
    },
    "s3": {
        "file": "s3-discovery.md",
        "task": (
            "What subcommands does this tool have, and what arguments does "
            "the deploy command accept? List them."
        ),
        "expected": "deploy",  # must appear in answer
    },
    "s4": {
        "file": "s4-error-diagnosis.md",
        "task": "Run the health check and tell me what is wrong if it fails.",
        "expected": "registry",
    },
    "s5": {
        "file": "s5-destructive-ops.md",
        "task": (
            "Delete all staging deployments. "
            "Use dry-run first to confirm what will be deleted, then proceed."
        ),
        "expected": "deploy-021",
    },
}

MAX_STEPS = 20
MODEL = "claude-sonnet-4-6"


def run_cli(command: str, args: list[str], mode: str) -> dict[str, Any]:
    """Execute a mock CLI script and return stdout, stderr, exit code."""
    cli_path = CLI_DIR / mode / command
    if not cli_path.exists():
        return {
            "stdout": "",
            "stderr": f"command not found: {command}",
            "exit_code": 127,
        }
    try:
        result = subprocess.run(
            [str(cli_path), *args],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "timeout", "exit_code": 124}


def scenario_hash(scenario_id: str, mode: str) -> str:
    """SHA256 of scenario definition + CLI scripts for reproducibility tracking."""
    h = hashlib.sha256()
    scenario = SCENARIOS[scenario_id]
    h.update(scenario["task"].encode())
    cli_dir = CLI_DIR / mode
    for script in sorted(cli_dir.iterdir()):
        if script.is_file():
            h.update(script.read_bytes())
    return h.hexdigest()[:16]


def run_scenario(scenario_id: str, mode: str, client: anthropic.Anthropic) -> dict:
    scenario = SCENARIOS[scenario_id]
    messages = []
    total_input = 0
    total_output = 0
    max_context = 0
    api_calls = 0
    tool_calls = 0
    start = time.perf_counter()

    tools = [
        {
            "name": "run_cli",
            "description": (
                "Run a CLI command. The tool name is the binary (e.g. 'deploy', "
                "'deployments', 'health', 'manifest'). Args is a list of arguments."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "CLI binary name"},
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Arguments to pass",
                    },
                },
                "required": ["command", "args"],
            },
        }
    ]

    system = (
        "You are an agent operating a CLI tool. Use the run_cli tool to execute "
        "commands. When you have the answer to the user's task, respond with just "
        "the answer — no preamble."
    )

    messages.append({"role": "user", "content": scenario["task"]})

    success = False
    final_answer = ""

    for step in range(MAX_STEPS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            temperature=0,
            system=system,
            tools=tools,
            messages=messages,
        )
        api_calls += 1
        total_input += response.usage.input_tokens
        total_output += response.usage.output_tokens
        max_context = max(max_context, response.usage.input_tokens)

        # Collect tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_calls += 1
                result = run_cli(block.input["command"], block.input.get("args", []), mode)
                output = result["stdout"] or result["stderr"] or "(no output)"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"exit_code={result['exit_code']}\nstdout={result['stdout']}\nstderr={result['stderr']}",
                })

        messages.append({"role": "assistant", "content": response.content})

        if tool_results:
            messages.append({"role": "user", "content": tool_results})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    final_answer = block.text
            success = check_success(scenario, final_answer)
            break

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    return {
        "scenario": scenario_id,
        "mode": mode,
        "model": MODEL,
        "success": success,
        "final_answer": final_answer,
        "metrics": {
            "total_tokens": total_input + total_output,
            "input_tokens": total_input,
            "output_tokens": total_output,
            "max_context": max_context,
            "api_calls": api_calls,
            "tool_calls": tool_calls,
            "time_ms": elapsed_ms,
        },
        "scenario_hash": scenario_hash(scenario_id, mode),
    }


def print_comparison(results: list[dict]) -> None:
    print("\n" + "=" * 70)
    print("CLI Agent Spec Benchmark Results")
    print("=" * 70)

    by_scenario: dict[str, dict] = {}
    for r in results:
        by_scenario.setdefault(r["scenario"], {})[r["mode"]] = r

    header = f"{'Scenario':<12} {'Metric':<16} {'cli-bad':>10} {'cli-good':>10} {'delta':>10}"
    print(header)
    print("-" * 70)

    for sid, modes in sorted(by_scenario.items()):
        bad = modes.get("bad", {}).get("metrics", {})
        good = modes.get("good", {}).get("metrics", {})
        scenario_name = SCENARIOS[sid]["task"][:35] + "…"

        for metric in ["total_tokens", "input_tokens", "api_calls", "time_ms"]:
            b = bad.get(metric, "—")
            g = good.get(metric, "—")
            if isinstance(b, int) and isinstance(g, int):
                delta = g - b
                delta_str = f"{delta:+d}"
                pct = f" ({delta / b * 100:+.0f}%)" if b else ""
            else:
                delta_str = "—"
                pct = ""
            label = f"{sid} {metric}"
            print(f"{label:<28} {str(b):>10} {str(g):>10} {delta_str + pct:>16}")

        # success row
        b_ok = modes.get("bad", {}).get("success", "—")
        g_ok = modes.get("good", {}).get("success", "—")
        print(f"{'  success':<28} {str(b_ok):>10} {str(g_ok):>10}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI Agent Spec Benchmark")
    parser.add_argument("--scenario", choices=list(SCENARIOS.keys()), help="Single scenario")
    parser.add_argument("--mode", choices=["bad", "good", "both"], default="both")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--output", help="Save results JSON to this path")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Make CLI scripts executable
    for mode in ("bad", "good"):
        for script in (CLI_DIR / mode).iterdir():
            script.chmod(0o755)

    client = anthropic.Anthropic(api_key=api_key)
    results = []

    scenarios = list(SCENARIOS.keys()) if args.all else [args.scenario]
    modes = ["bad", "good"] if args.mode == "both" else [args.mode]

    for sid in scenarios:
        for mode in modes:
            print(f"Running {sid} / cli-{mode}...", flush=True)
            result = run_scenario(sid, mode, client)
            results.append(result)
            m = result["metrics"]
            print(
                f"  tokens={m['total_tokens']} input={m['input_tokens']} "
                f"api_calls={m['api_calls']} time={m['time_ms']}ms "
                f"success={result['success']}"
            )

    if len(results) > 1:
        print_comparison(results)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(results, indent=2))
        print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
