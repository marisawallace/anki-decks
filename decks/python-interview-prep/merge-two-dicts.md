---
id: "a8de39ef8a69489da5b94a2b976c982f"
tags: [dict, syntax]
---

# Front
Merge two dicts

# Back
`{**a, **b}` (b wins on conflicts), or `a | b` (3.9+), or `a.update(b)` (mutates a).
