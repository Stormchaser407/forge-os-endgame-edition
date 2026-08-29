## 2026-04-28 - Missing Timeout in `requests.get`
**Vulnerability:** Found a call to `requests.get` missing a timeout argument in `oracle.py`.
**Learning:** `requests.get` without a timeout can hang indefinitely, causing resource exhaustion or Denial of Service.
**Prevention:** Always include a `timeout` parameter in external network calls like `requests.get()`.
