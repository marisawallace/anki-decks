---
id: "c48f13b39a5c4ea0abfc75c3c0497f1b"
tags: [ruby-diff, comprehension]
---

# Front
Map a function over a list (Ruby: `arr.map { ... }`)

# Back
List comprehension: `[f(x) for x in arr]` — Slatkin: prefer this. Reach for `list(map(f, arr))` only when `f` is an existing named function.
