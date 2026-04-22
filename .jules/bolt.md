## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.
## 2026-04-22 - Pre-compile Regex and Use Combined Fast-Path
**Learning:** For multi-pattern regex matching on large datasets where matches are rare, avoid inline imports (`import re`) inside hot paths to prevent function call and import overhead. Also, compiling regexes individually inside loops is inefficient.
**Action:** Move module imports to the top level. Pre-compile regex patterns during object initialization. Additionally, compile a combined regex using `|` to act as a fast-path `.search()` guard, skipping individual matching loops for non-matching content entirely.
