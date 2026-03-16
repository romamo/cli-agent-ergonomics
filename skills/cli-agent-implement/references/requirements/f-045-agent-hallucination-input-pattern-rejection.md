# REQ-F-045: Agent Hallucination Input Pattern Rejection

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§35 Agent Hallucination Input Patterns](../challenges/01-critical-ecosystem-runtime-agent-specific/35-high-hallucination-inputs.md)

**Addresses:** Severity: High / Token Spend: High / Time: High / Context: Medium

---

## Description

The framework MUST automatically validate all arguments declared as resource IDs, paths, or identifiers against a set of known agent hallucination patterns. The following patterns MUST be rejected with exit code 2 before any side effect: path traversal sequences (`../`, `..%2f`, `..%5c`, `%2e%2e/`), percent-encoded segments in resource IDs (`%2e`, `%2f`, `%40`), embedded query parameters (`?`, `&` in resource IDs), fragment identifiers (`#` in resource IDs), and URL-encoded shell metacharacters. Command authors declare the argument type; the framework applies appropriate pattern checks automatically.

## Acceptance Criteria

- An argument of type `resource_id` containing `../` is rejected in Phase 1 with exit code 2.
- An argument containing `%2e%2e` is rejected in Phase 1 with exit code 2.
- An argument containing `?foo=bar` where `?` is not expected is rejected with exit code 2.
- A path argument that is valid (e.g., `/home/user/file.txt`) passes validation without modification.
