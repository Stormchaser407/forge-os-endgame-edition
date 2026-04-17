## 2026-04-17 - Missing Timeout in Network Request
**Vulnerability:** External network request without a timeout parameter could lead to DoS vulnerabilities via hanging connections.
**Learning:** In `oracle.py` and similar places where `requests.get()` is used, failing to provide a timeout parameter allows network operations to run indefinitely, leading to resource exhaustion.
**Prevention:** Always include a `timeout` parameter (e.g., `timeout=30`) in external network calls like `requests.get()`.