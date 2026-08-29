## 2026-04-22 - Missing Timeout in Network Request
**Vulnerability:** Missing timeout configuration in `requests.get()` in `obsidian-council/agents/identity/oracle.py`.
**Learning:** External network calls using `requests` without explicit timeouts can block indefinitely if the remote server hangs, leading to thread/resource exhaustion and Denial of Service (DoS) vulnerabilities (`[B113:request_without_timeout]`).
**Prevention:** Always enforce explicit, reasonable timeouts (`timeout=X`) on all external HTTP requests made via libraries like `requests` to ensure applications fail fast and release resources securely.
