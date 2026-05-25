---
id: "b0697341cfd04804ac04d01421ad0e28"
tags: [footgun, list, perf]
---

# Front
Footgun: list.pop(0) / list.insert(0, x) are O(n)

# Back
Both shift every element. For a FIFO queue use `collections.deque` — `append`/`popleft` are O(1).
