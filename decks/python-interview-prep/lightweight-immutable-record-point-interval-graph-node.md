---
id: "fb42fa3da7504ee3bbe8541fb28fa83e"
tags: [stdlib, slatkin, record]
---

# Front
Lightweight immutable record (point, interval, graph node)

# Back
`from collections import namedtuple; Point = namedtuple("Point", "x y")`. Immutable, hashable (usable as a dict key / set element), tuple-unpackable: `x, y = p`.
