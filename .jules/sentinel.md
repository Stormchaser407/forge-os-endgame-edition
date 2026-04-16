## 2026-04-16 - [Resource Exhaustion / DoS Vulnerability in Requests]
**Vulnerability:** External HTTP requests made without a timeout parameter (e.g. `requests.get()`) can hang indefinitely, leading to resource exhaustion or a Denial of Service (DoS) attack.
**Learning:** This existed because the timeout parameter is not strictly enforced by the standard requests library by default.
**Prevention:** Always explicitly define a timeout (e.g. `timeout=30`) for external network calls to ensure they fail securely instead of blocking resources indefinitely.
