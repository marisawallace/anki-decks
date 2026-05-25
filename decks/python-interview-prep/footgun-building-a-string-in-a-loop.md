---
id: "da2544b14af54ee8a533443f0ad0b431"
tags: [footgun, string, perf]
---

# Front
Footgun: building a string in a loop

# Back
`s += piece` in a loop is O(n²) — strings are immutable, so each `+=` copies the whole string. Collect pieces in a list and `"".join(parts)` (O(n)).
