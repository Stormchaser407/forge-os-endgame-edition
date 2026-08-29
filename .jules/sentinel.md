## 2026-04-30 - Add timeout to requests.get in oracle.py
**Vulnerability:** A `requests.get` call was missing a `timeout` parameter, which could lead to indefinite hanging if the target server was unresponsive.
**Learning:** This is a common pattern that can lead to Denial of Service (DoS) vulnerabilities due to resource exhaustion.
**Prevention:** Always include a `timeout` parameter in external network calls like `requests.get()`.
