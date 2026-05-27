---
id: "b0697341cfd04804ac04d01421ad0e28"
tags: [footgun, list, perf]
---

# Front
Footgun: list.pop(0) / list.insert(0, x) are O(n)

# Back
Both shift every element to fill/make room at index 0.

Under the hood, a CPython `list` is a **dynamic array** (contiguous array of `PyObject*` with geometric over-allocation) — *not* a linked list. So:

| op | cost | why |
|---|---|---|
| `list.append(x)` | **amortized O(1)** | writes to the pre-allocated tail; occasional resize is amortized away |
| `list.pop()` (end) | **O(1)** | just decrements length |
| `list[i]` | **O(1)** | pointer arithmetic into the array |
| `list.pop(0)` | **O(n)** | shifts all n−1 trailing elements left by one |
| `list.insert(0, x)` | **O(n)** | shifts all n existing elements right by one (plus possible resize) |

For a FIFO queue use `collections.deque` (doubly-linked blocks) — `append`/`appendleft`/`pop`/`popleft` are all O(1).
