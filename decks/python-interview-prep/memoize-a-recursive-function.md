---
id: "804b68b673c045d289f94c5d7db6693b"
tags: [stdlib]
---

# Front
Memoize a recursive function

# Back
`from functools import cache` (or `lru_cache(maxsize=None)`); decorate with `@cache`. Great for DP/recursion.
