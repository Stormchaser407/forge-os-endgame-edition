## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.
## 2026-04-24 - Pre-compile regexes with fast-path search
**Learning:** In hot loops, repeated regular expression compilation and matching can be a severe bottleneck. For multi-pattern regex matching on large datasets where matches are rare, inline imports and re-compiling expressions in loops severely drag down performance.
**Action:** Optimize by pre-compiling a combined regex (using `|`) to act as a 'fast-path' search. Use `.search()` on the combined pattern to skip individual matching loops for non-matching content. Move all `import re` statements to the module level.
## 2026-04-25 - Avoid Assumptions During Exploration
**Learning:** When using commands like `grep`, `head`, or `tail` to explore files, it is easy to incorrectly assume the names of enclosing functions or methods if they are not explicitly visible in the output trace.
**Action:** Verify the exact context using `read_file` before referencing functions in an execution plan to avoid violating the Groundedness Rule.
