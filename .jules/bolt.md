## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.
## 2026-04-24 - Pre-compile regexes with fast-path search
**Learning:** In hot loops, repeated regular expression compilation and matching can be a severe bottleneck. For multi-pattern regex matching on large datasets where matches are rare, inline imports and re-compiling expressions in loops severely drag down performance.
**Action:** Optimize by pre-compiling a combined regex (using `|`) to act as a 'fast-path' search. Use `.search()` on the combined pattern to skip individual matching loops for non-matching content. Move all `import re` statements to the module level.
## 2026-04-28 - Fast-Path Regex Grouping Precedence
**Learning:** When combining regex patterns with the '|' operator for fast-path searches (e.g., '|'.join(patterns)), '|' has the lowest precedence in Python's 're' module. Unintended concatenation parsing can occur if individual patterns lack explicit boundaries.
**Action:** Ensure individual patterns are explicitly grouped with non-capturing groups `(?:...)` before joining to preserve exact regex semantics and precedence.

## 2026-04-28 - Scope Creep on Module Imports
**Learning:** Attempting to fix "improper" directory names (like `social-media` to `social_media`) during a performance task leads to breaking imports and violates the constraint against making breaking or architectural changes.
**Action:** Stick strictly to the targeted optimization. Use `PYTHONPATH` manipulation if needed for local benchmarking rather than permanently renaming directories.
