## 2026-05-03 - Fix missing timeout in external network call
**Vulnerability:** External network calls via `requests.get()` without a timeout parameter.
**Learning:** This exposes the application to uncontrolled resource consumption and Denial of Service (DoS) vulnerabilities via hanging requests if the external server is unresponsive.
**Prevention:** Always include a `timeout` parameter (e.g., `requests.get(..., timeout=10)`) when making external network calls using the `requests` library.
