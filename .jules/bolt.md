## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.
## 2026-04-19 - Pre-compile Regex and Avoid Inline Imports in Text Processing
**Learning:** Calling `import` inline inside a frequently called function (like NLP text extraction) adds unnecessary function call and lookup overhead. In addition, repeatedly compiling regex patterns inside text processing loops degrades performance.
**Action:** Move all module imports to the file level. Pre-compile regex patterns (with any necessary flags like `re.IGNORECASE`) in the `__init__` method and reuse the compiled pattern objects in hot paths.
