
## 2026-04-20 - [Missing timeout in external requests]
**Vulnerability:** A call to `requests.get()` without a timeout parameter in `oracle.py` image download function (`B113:request_without_timeout`).
**Learning:** External network calls can hang indefinitely if the remote server doesn't respond, leading to resource exhaustion (e.g. threads, connections, memory) and potential Denial of Service (DoS) vulnerabilities in the application processing the requests.
**Prevention:** Always include a `timeout` parameter in external network calls (e.g., `requests.get(url, timeout=10)`) to prevent unbounded waiting and resource starvation.
