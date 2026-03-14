> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §67

## 67. Agent-Generated Input Syntax Rejection

**Source:** Antigravity `07_schema_and_discoverability.md` (RA)

**Severity:** High | **Frequency:** Common | **Detectability:** Easy | **Token Spend:** High | **Time:** Medium | **Context:** Low

### The Problem

LLMs frequently generate near-valid structured input that strict parsers reject: JSON with trailing commas, inline comments, unquoted keys, or minor whitespace variations that are valid in JSON5 or YAML but invalid in strict JSON. A tool that accepts `--config '{"key": "value"}'` but rejects `--config '{"key": "value",}'` (trailing comma) fails immediately. The agent must then debug a parse error in its own generated content — spending reasoning tokens on a meta-level failure rather than the actual task.

```bash
# LLM generates JSON with trailing comma (very common LLM output pattern):
$ tool create --config '{"name": "prod", "region": "us-east-1",}'
Error: Invalid JSON: Unexpected token } at position 38
# Agent must now reason about JSON syntax, not the task

# LLM includes a comment (natural for LLM to explain its reasoning):
$ tool create --config '{"name": "prod" /* production environment */}'
Error: Invalid JSON: Unexpected token / at position 16

# LLM generates unquoted keys (also common):
$ tool create --config '{name: "prod", region: "us-east-1"}'
Error: Invalid JSON: Unexpected token n at position 1

# Each error requires a round trip: agent must reformat and retry
```

The pattern repeats across configuration flags, filter expressions, template strings, and any structured input the agent must generate.

### Impact

- Round trip cost: agent must diagnose parse error, reformat input, retry
- Reasoning tokens wasted on JSON syntax rather than the actual task
- High frequency: LLMs naturally produce JSON5-ish output, especially when generating longer JSON objects
- Cascading: multiple retries before the agent produces perfectly strict JSON

### Solutions

**Accept JSON5 / forgiving JSON for all structured inputs:**
```python
import json5  # pip install json5
config = json5.loads(user_input)
# Accepts: trailing commas, comments, unquoted keys, single quotes
```

**Normalize before parsing:**
```python
import re
def normalize_json(s):
    s = re.sub(r',\s*([}\]])', r'\1', s)   # remove trailing commas
    s = re.sub(r'//.*?$', '', s, flags=re.M)  # remove line comments
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)  # remove block comments
    return json.loads(s)
```

**Surface clear correction in error:**
```json
{
  "ok": false,
  "error": {
    "code": "INVALID_JSON",
    "message": "Trailing comma at line 1, position 38.",
    "corrected_input": "{\"name\": \"prod\", \"region\": \"us-east-1\"}",
    "hint": "Remove trailing comma after last key-value pair."
  }
}
```

**For framework design:**
- Framework MUST use a forgiving JSON parser (JSON5 or equivalent) for all `--config`, `--filter`, `--data`, and `--raw-payload` flag inputs.
- When strict JSON is required (e.g., for schema validation), the framework normalizes the input before validation and emits the corrected form in the error if validation fails.
- The `corrected_input` field in parse errors enables agents to retry with minimal reasoning.
