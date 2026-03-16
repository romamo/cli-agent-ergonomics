# REQ-F-036: HTTP Client Proxy Environment Variable Compliance

**Tier:** Framework-Automatic | **Priority:** P1

**Source:** [§31 Network Proxy Unawareness](../challenges/05-high-environment-and-state/31-high-network-proxy.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: High / Context: Low

---

## Description

The framework's built-in HTTP client MUST automatically read and apply `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables. The framework MUST support proxy authentication (credentials in proxy URL). The framework MUST use the system certificate store or a configurable CA bundle path (respecting `REQUESTS_CA_BUNDLE` or `SSL_CERT_FILE` environment variables). These behaviors MUST be on by default with no additional configuration from command authors.

## Acceptance Criteria

- When `HTTPS_PROXY` is set, all outbound HTTPS requests from the framework's HTTP client use that proxy.
- When `NO_PROXY=localhost`, requests to `localhost` bypass the proxy.
- When `REQUESTS_CA_BUNDLE` is set, the specified CA bundle is used for SSL verification.
- A command author who uses the framework's HTTP client does not need to write any proxy handling code.
