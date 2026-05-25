---
id: "2c4840eba4474644a8997718bf7c04ac"
tags: [stdlib, footgun]
---

# Front
Min-heap: push, pop, and the max-heap gotcha

# Back
`import heapq; heapq.heappush(h, x); heapq.heappop(h)` → smallest. Python has ONLY a min-heap — for a max-heap push `-x` (or use a key tuple).
