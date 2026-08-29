
## 2026-04-23 - Missing Timeout in Requests
**Vulnerability:** External API call `requests.get` in `oracle.py` was missing a timeout parameter (`[B113:request_without_timeout]`).
**Learning:** External network calls without a timeout can lead to uncontrolled resource consumption and Denial of Service (DoS) vulnerabilities if the remote server hangs or responds very slowly.
**Prevention:** Always include a `timeout` parameter (e.g., `timeout=10`) in all network requests (e.g., `requests.get`, `requests.post`) to ensure they fail gracefully.
