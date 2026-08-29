## 2024-05-04 - [Missing Timeout on External Network Call]
**Vulnerability:** The `requests.get()` method was used to download images from external URLs without a `timeout` parameter in `obsidian-council/agents/identity/oracle.py`.
**Learning:** Python`s `requests` library does not apply a timeout by default. If a remote server is unresponsive or deliberately holds the connection open, the thread will hang indefinitely. This can lead to resource exhaustion and a Denial of Service (DoS) condition if many requests hang simultaneously.
**Prevention:** Always explicitly define a `timeout` parameter (e.g., `timeout=10`) when making network requests using libraries like `requests`, `urllib`, or `aiohttp` to ensure the application fails fast and gracefully handles slow or malicious servers.
