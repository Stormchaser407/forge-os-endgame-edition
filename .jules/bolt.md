## 2026-04-16 - Prevent Redundant String Allocations in Core Base Classes
**Learning:** To prevent redundant O(N*M) string allocation overhead, precompute static `.lower()` transformations and object properties outside of hot loops.
**Action:** Precompute properties like `self.codename_lower` in the `__init__` method and cache them for reuse.
## 2026-04-24 - Pre-compile regexes with fast-path search
**Learning:** In hot loops, repeated regular expression compilation and matching can be a severe bottleneck. For multi-pattern regex matching on large datasets where matches are rare, inline imports and re-compiling expressions in loops severely drag down performance.
**Action:** Optimize by pre-compiling a combined regex (using `|`) to act as a 'fast-path' search. Use `.search()` on the combined pattern to skip individual matching loops for non-matching content. Move all `import re` statements to the module level.
## 2026-05-04 - Offloading synchronous external calls in async methods
**Learning:** Synchronous calls to external libraries (like `geopy`'s `Nominatim.geocode` and `reverse_geocoder.search`) inside `async` methods block the event loop, causing severe performance bottlenecks by starving concurrent tasks.
**Action:** Always offload synchronous network or disk-bound calls within async contexts to a thread pool using `await asyncio.to_thread(...)` or `loop.run_in_executor(None, ...)`.
