# REQ-O-019: --proxy and --no-proxy Flags

**Tier:** Opt-In | **Priority:** P2

**Source:** [§31 Network Proxy Unawareness](../challenges/05-high-environment-and-state/31-high-network-proxy.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

The framework MUST provide `--proxy <url>` (override proxy for this invocation) and `--no-proxy` (bypass proxy for this invocation) as standard flags on all commands that perform network I/O. `--proxy` MUST override `HTTPS_PROXY` and `HTTP_PROXY` environment variables. `--no-proxy` MUST bypass all proxy settings (direct connection). These flags MUST be automatically available on commands that declare `has_network_io: true`.

## Acceptance Criteria

- `--proxy http://proxy.example.com:8080` routes all HTTP requests through that proxy.
- `--no-proxy` results in direct connections regardless of `HTTPS_PROXY` env var.
- The proxy URL used is reflected in `network_context` in error responses.
- The flags are absent on commands that declare no network I/O.
