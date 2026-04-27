## 2025-02-27 - Missing timeout in external request
**Vulnerability:** External HTTP request via `requests.get` without a timeout in `obsidian-council/agents/identity/oracle.py`
**Learning:** Network calls without explicit timeouts can lead to application hangs, resource exhaustion, and potential Denial of Service (DoS) if the target server is slow or unresponsive.
**Prevention:** Always include a `timeout` parameter (e.g., `timeout=10`) when using `requests.get()` or similar external network call functions.
