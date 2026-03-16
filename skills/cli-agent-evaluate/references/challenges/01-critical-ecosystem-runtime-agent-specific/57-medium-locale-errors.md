> **Part VII: Ecosystem, Runtime & Agent-Specific** | Challenge §57

## 57. Locale-Dependent Error Messages

**Severity:** Medium | **Frequency:** Situational | **Detectability:** Easy | **Token Spend:** High | **Time:** Low | **Context:** Medium

### The Problem

Distinct from §2 (locale-invariant serialization of numbers/dates), many CLI tools embed raw OS or runtime error messages directly in `error.message`. These come from `errno`, OS exceptions, database drivers — and they are locale-translated. On a French server, "Permission denied" becomes "Permission refusée". Agents that pattern-match on error message text fail silently in non-English environments.

```python
try:
    os.rename(src, dst)
except OSError as e:
    return {"ok": False, "error": {"message": str(e)}}
# en_US: "Permission denied: '/etc/hosts'"
# fr_FR: "Permission refusée: '/etc/hosts'"
# Agent checking for "Permission denied" fails on French systems
```

### Impact

- Error-handling logic that pattern-matches on message text fails on non-English systems
- Agents may retry indefinitely when error classification fails

### Solutions

**Separate machine-readable code from locale message:**
```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "Permission denied: '/etc/hosts'",
    "locale_message": "Permission refusée: '/etc/hosts'",
    "locale": "fr_FR"
  }
}
```

**Framework normalizes OS errors to English (`LC_MESSAGES=C`) before serialization.**

**For framework design:**
- The framework's exception handler MUST normalize all OS/runtime error messages to English before placing them in `error.message`.
- `error.code` is the ONLY field agents should use for error classification; `error.message` is human-readable context only.
