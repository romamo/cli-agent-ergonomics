---
name: codegen-setup
description: Install JSON Schema codegen tools and generate language-specific types from schemas/. Use when the user asks how to install codegen tools, generate types/models/structs from schemas, set up ajv validation, or get started with schema-driven development for Python, TypeScript, Rust, Go, or Java.
tools: Bash, Read
---

# Schema Codegen Setup

Read [`schemas/codegen-guide.md`](../../../schemas/codegen-guide.md) fully, then help the user through the workflow for their language. If the user needs broader implementation context, point them to [`IMPLEMENTING.md`](../../../IMPLEMENTING.md).

## Steps

1. If the user has not stated a language, ask: "Which language are you targeting — Python, TypeScript, Rust, Go, or Java?"

2. Check what is already installed:

```bash
node --version 2>/dev/null || echo "node: NOT INSTALLED"
ajv --version 2>/dev/null || echo "ajv-cli: NOT INSTALLED"
python3 --version 2>/dev/null || echo "python3: NOT INSTALLED"
datamodel-codegen --version 2>/dev/null || echo "datamodel-code-generator: NOT INSTALLED"
json2ts --version 2>/dev/null || echo "json-schema-to-typescript: NOT INSTALLED"
cargo --version 2>/dev/null || echo "cargo: NOT INSTALLED"
go version 2>/dev/null || echo "go: NOT INSTALLED"
java --version 2>/dev/null || echo "java: NOT INSTALLED"
```

3. Show only the install commands the user needs (skip anything already installed). Always include `ajv-cli` if missing — it is required for all languages.

4. After installation, show the validate command, then the generate command for the user's language. Both are in the guide.

5. Remind the user to add the `ExitCodeEntry` invariant validation for their language (snippet in the guide under "Validation after generation").

Do not modify any files — this skill is install and run guidance only.
