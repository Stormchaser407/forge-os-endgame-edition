## 2025-05-24 - Insecure Temp Directory in Map Generation
**Vulnerability:** Hardcoded `/tmp/` directory path used for saving map visualizations in atlas.py.
**Learning:** Using predictable paths in `/tmp/` creates race condition and symlink vulnerabilities.
**Prevention:** Always use `tempfile.mkstemp()` or `tempfile.TemporaryDirectory()` for secure temporary file creation.
