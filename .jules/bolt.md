## 2024-05-15 - Regex Compilation Strategy
**Learning:** Pre-compiling regex patterns inside loops/frequent methods has a measurable impact on Python performance, specifically in `ARGUS` social media polling loops and `audit_runner` scripts. For example, moving `re.compile()` out of inner loops for extracting hashtags/mentions yields ~2x speedup in parsing text loops.
**Action:** When finding `re.findall`, `re.search` or similar regex calls inside loops or frequently instantiated classes, extract them to class level or module level `re.compile()` calls.
