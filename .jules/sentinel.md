## 2024-05-20 - Missing Timeout in requests.get
**Vulnerability:** A network request using requests.get() was made without specifying a timeout parameter in obsidian-council/agents/identity/oracle.py.
**Learning:** External network calls can hang indefinitely if the server is unresponsive, leading to resource exhaustion, thread blocking, and potential Denial of Service (DoS).
**Prevention:** Always include a timeout parameter (e.g., timeout=10) when using requests.get() or similar functions to ensure the application fails fast and securely.
## 2024-05-20 - Insecure Usage of Hardcoded Temporary Directory
**Vulnerability:** Multiple agents (atlas.py, argus.py) use hardcoded, predictable temporary directories like '/tmp/atlas_map_...' or '/tmp/argus-screenshots' for saving sensitive output (maps, screenshots).
**Learning:** Hardcoding '/tmp' directories creates predictability. Predictable temporary files can lead to symlink attacks, race conditions, and potentially expose sensitive investigation data to unauthorized local users. This violates CWE-377 and the [B108:hardcoded_tmp_directory] check.
**Prevention:** Always use secure, randomized temporary directory generation provided by the standard library, such as tempfile.mkdtemp(prefix=...) or tempfile.TemporaryDirectory(), to prevent predictable temporary paths and ensure data isolation.
