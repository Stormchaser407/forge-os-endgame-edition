## 2024-05-02 - [Denial of Service via Unbounded Network Request]
**Vulnerability:** The codebase was performing external network requests via `requests.get` without providing a timeout parameter.
**Learning:** This existed because standard library usage examples often omit the timeout, but in production, remote servers can hang indefinitely.
**Prevention:** Always provide a `timeout` parameter (e.g., `requests.get(..., timeout=10)`) to external network calls to prevent resource exhaustion.
