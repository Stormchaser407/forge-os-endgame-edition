## 2026-04-15 - Redundant Regex Compilation in Hot Paths
**Learning:** Found repetitive dynamic regex compilation and inline imports (`import re`) inside a frequently called NLP extraction method `_extract_location_mentions`. While Python internally caches some `re` patterns, the function call overhead and inline imports inside loops or hot paths add up.
**Action:** Move module imports to the top level and pre-compile static regular expressions into instance variables (e.g. `self._compiled_location_patterns = [...]`) during `__init__` to minimize execution time inside hot paths.
