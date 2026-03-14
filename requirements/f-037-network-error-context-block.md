# REQ-F-037: Network Error Context Block

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§31 Network Proxy Unawareness](../challenges/05-high-environment-and-state/31-high-network-proxy.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

When any network operation fails, the framework MUST include a `network_context` block in the error object containing: `proxy_used` (URL or null), `proxy_source` (which env var or config), `no_proxy` (value or null), `ssl_verify` (boolean), and a `suggestion` field with a concrete diagnostic command. This block MUST be populated by the framework automatically without command author effort.

## Acceptance Criteria

- A connection failure error includes `error.network_context.proxy_used`.
- When no proxy is configured, `error.network_context.proxy_used` is null (not absent).
- `error.network_context.suggestion` contains an executable shell command for diagnosing the failure.
- The network_context block is absent for non-network errors.
