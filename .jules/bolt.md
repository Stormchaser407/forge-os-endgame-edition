## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.
## 2026-04-16 - Fast-path Combined Regex Optimization
**Learning:** For multi-pattern regex matching on large datasets where matches are rare, iterating over all patterns individually incurs high overhead.
**Action:** Pre-compile a combined regex using '|' and use `.search()` as a 'fast-path' to skip non-matching content before iterating over individual patterns.
