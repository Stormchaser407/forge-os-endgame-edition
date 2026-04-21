## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.
## 2025-05-15 - Fast-Path Combined Regex Guards
**Learning:** For multi-pattern regex matching on large datasets where matches are rare, iterating over individual patterns is a performance bottleneck.
**Action:** Optimize by pre-compiling a combined regex (using '|') to act as a 'fast-path' search. Use `.search()` on the combined pattern to skip individual matching loops for non-matching content.
