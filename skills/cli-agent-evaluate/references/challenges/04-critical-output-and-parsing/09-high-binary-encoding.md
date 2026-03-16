> **Part I: Output & Parsing** | Challenge §9

## 9. Binary & Encoding Safety

**Severity:** High | **Frequency:** Situational | **Detectability:** Hard | **Token Spend:** Low | **Time:** Medium | **Context:** Low

### The Problem

CLI tools that read files, databases, or APIs may encounter binary data, null bytes, or non-UTF-8 strings. When this data is embedded in JSON output, serialization silently corrupts or crashes the tool, and the agent receives either invalid JSON or a crash with no result.

**Null bytes break JSON:**
```bash
$ tool read-file binary.bin --output json
# File contains \x00 bytes
# json.dumps() in Python: works but produces \u0000
# json.loads() in some parsers: terminates string at \x00
# Result: agent gets truncated or invalid data silently
```

**Non-UTF-8 crashes serialization:**
```bash
$ tool read-file latin1-encoded.txt --output json
# File is Latin-1, not UTF-8
# Python json.dumps(): UnicodeDecodeError → unhandled → crash
# Agent receives: empty stdout, exit 1, no JSON error
```

**Binary in API response:**
```bash
$ tool fetch-record --id 42 --output json
# Record's "avatar" field contains raw PNG bytes
# JSON serialization: fails or produces garbage
# Agent: receives malformed JSON
```

**Log files with mixed encoding:**
```bash
$ tool get-logs --output json
# Log file has 99% UTF-8, one line with a Latin-1 char
# Tool crashes on that line, returns partial output
# Agent: partial JSON, parse error
```

### Impact

- Tool crashes with no JSON error output (agent gets empty stdout)
- JSON is malformed — agent's JSON parser throws
- Binary data silently truncated — agent gets wrong data, no warning
- Non-deterministic behavior depending on data content

### Solutions

**Detect and handle encoding explicitly:**
```python
def safe_read(path: str) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        # Return base64 for binary, with metadata
        return None  # signal: use binary path

def safe_field(value: bytes | str) -> dict:
    if isinstance(value, bytes):
        try:
            text = value.decode("utf-8")
            return {"type": "text", "value": text}
        except UnicodeDecodeError:
            import base64
            return {"type": "binary", "encoding": "base64",
                    "value": base64.b64encode(value).decode()}
    return {"type": "text", "value": value}
```

**Binary fields use base64 in JSON output:**
```json
{
  "ok": true,
  "data": {
    "name": "photo.png",
    "content": {
      "type": "binary",
      "encoding": "base64",
      "value": "iVBORw0KGgo...",
      "size_bytes": 45231
    }
  }
}
```

**Null byte sanitization:**
```python
def sanitize_string(s: str) -> str:
    return s.replace("\x00", "\ufffd")  # replacement character
```

**Declare content type in output:**
```json
{
  "data": {
    "content": "...",
    "content_encoding": "utf-8",    // or "base64", "latin-1"
    "content_type": "text/plain"    // or "application/octet-stream"
  }
}
```

**For framework design:**
- All string fields pass through a UTF-8 sanitizer before JSON serialization
- Binary fields automatically base64-encoded with `{type, encoding, value}` wrapper
- Framework catches UnicodeDecodeError and emits structured error, never crashes raw
- `--binary-mode base64|hex|skip` flag for commands that may return binary

---
