---
id: "411ba38d3a6c433095d95d70d354b53e"
tags: [stdlib, sorting, slatkin]
---

# Front
Put custom objects in a heap or sorted list

# Back
`heapq`/`sorted` compare with `<`. Give the class `@dataclass(order=True)`, or push `(priority, item)` tuples (ties break left-to-right), or define `__lt__`.
