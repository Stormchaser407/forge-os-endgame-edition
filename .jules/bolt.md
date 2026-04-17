## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.## 2026-04-17 - Prevent redundant inline module imports inside hot loops
**Learning:** Avoid inline module imports (e.g., `import re`) inside frequently called functions or hot paths to prevent function call and import overhead.
**Action:** Move these imports to the module level instead.

## 2026-04-17 - Precompute lowercase property outside loops
**Learning:** Similar to string allocations inside core classes, performance overhead with `O(N*M)` execution logic (e.g., `_analyze_potential_matches`) occur if properties like `.lower()` are iteratively called inside the loop.
**Action:** Precompute static `property.lower()` loop values before passing execution to loops.
