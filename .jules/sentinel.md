## 2026-05-01 - Missing Timeout in External API Request
**Vulnerability:** External network request (`requests.get`) was missing a timeout parameter.
**Learning:** This exposes the application to resource exhaustion and potential Denial of Service (DoS) if the external server is unresponsive, causing the thread to hang indefinitely.
**Prevention:** Always use a `timeout` parameter in HTTP requests, like `requests.get(url, timeout=10)`.
