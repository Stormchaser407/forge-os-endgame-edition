## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.

## 2024-06-15 - Fast-Path Multi-Pattern Regex Checking
**Learning:** For multi-pattern text scanning operations (like analyzing social media posts for trafficking/distress indicators), sequentially running multiple `.findall()` loops on strings that contain no matches is extremely costly. Pre-compiling a combined regular expression (joined by `|`) provides a fast path to quickly rule out non-matching content, bypassing the expensive loops altogether.
**Action:** Always pre-compile a single combined regex using `re.compile('|'.join(...))` and use `.search()` as a fast-path guard before iterating through detailed individual pattern matching when processing large text datasets.
