---
id: "2c4840eba4474644a8997718bf7c04ac"
tags: [stdlib, footgun]
---

# Front
Min-heap: push, pop, and the max-heap gotcha

# Back
`import heapq`. The heap is just a plain `list` — init with `h = []` (or `heapq.heapify(existing_list)` to convert in-place in O(n)). No `Heap` class.

`heapq.heappush(h, x); heapq.heappop(h)` → smallest.

Items must be **mutually comparable** (`<` defined between them): numbers, strings, or tuples of comparable things. For custom objects either implement `__lt__` or push `(priority, tiebreaker, obj)` tuples — the tiebreaker (e.g. an incrementing counter) avoids comparing the objects when priorities tie.

Python has ONLY a min-heap — for a max-heap push `-x` (or negate the priority in the tuple).
