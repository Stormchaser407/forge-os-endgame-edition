## 2025-05-15 - Missing timeout in requests.get
**Vulnerability:** A `requests.get` call inside `obsidian-council/agents/identity/oracle.py` lacks a timeout parameter, potentially leading to a hanging request if the external server is unresponsive.
**Learning:** Missing timeouts can lead to unbounded resource consumption, effectively creating a Denial of Service (DoS) condition. It exists because the default behavior of `requests.get` blocks indefinitely without a timeout parameter.
**Prevention:** Always specify a `timeout` argument in external HTTP calls to ensure fail-safe behavior.
## 2025-05-15 - Hardcoded /tmp directory in argus.py
**Vulnerability:** The `self.screenshot_dir` is hardcoded to `/tmp/argus-screenshots` in `obsidian-council/agents/social-media/argus.py`, posing a security risk.
**Learning:** Hardcoded temporary directories in shared locations like `/tmp` are susceptible to symlink attacks, race conditions, and unauthorized data access.
**Prevention:** Use secure temporary directory generation techniques like `tempfile.mkdtemp()` or `tempfile.TemporaryDirectory()` to create unique, isolated directories.
## 2025-05-15 - Hardcoded /tmp directory in atlas.py
**Vulnerability:** The `map_path` uses a hardcoded `/tmp` directory path string `"/tmp/atlas_map_{case_id}_{datetime.now().strftime(%Y%m%d_%H%M%S)}.html"` in `obsidian-council/agents/geolocation/atlas.py`, posing a security risk.
**Learning:** Hardcoded temporary directories in shared locations like `/tmp` are susceptible to symlink attacks, race conditions, and unauthorized data access.
**Prevention:** Use secure temporary directory generation techniques like `tempfile.gettempdir()` combined with random generation, or directly use `tempfile.NamedTemporaryFile()`/`tempfile.mkdtemp()` to create unique, isolated files/directories.
