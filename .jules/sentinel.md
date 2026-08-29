## 2026-04-21 - [B108] Insecure Hardcoded Temporary Directory Usage
**Vulnerability:** Found hardcoded temporary directory (`/tmp/argus-screenshots`) usage in `argus.py` during evidence collection directory initialization.
**Learning:** Hardcoded temporary paths in shared directories like `/tmp` can lead to local privilege escalation or denial-of-service via symlink attacks (race conditions). They bypass the OS's secure temporary directory mechanisms.
**Prevention:** Always use secure library features like `tempfile.gettempdir()` or `tempfile.TemporaryDirectory()` rather than directly hardcoding paths to `/tmp` or other shared folders.
