## 2024-05-15 - Missing request timeout in Oracle Agent
**Vulnerability:** External requests were made without a timeout parameter in `obsidian-council/agents/identity/oracle.py` and potentially other files.
**Learning:** Network calls without explicit timeouts can lead to application hangs, resource exhaustion, and potential Denial of Service (DoS) if the remote server is unresponsive.
**Prevention:** Always include a `timeout` parameter in external network calls like `requests.get()` or `requests.post()` to ensure the application fails gracefully.
