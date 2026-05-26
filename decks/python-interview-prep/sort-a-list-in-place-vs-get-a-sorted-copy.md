---
id: "33fa3d0940734cf29d0669d3b9a64bf4"
tags: [sorting, footgun]
---

# Front
Sort a list in place vs. get a sorted copy

# Back
`lst.sort()` mutates (lists only), returns `None`. `sorted(iterable)` returns a new list and works on any iterable.
