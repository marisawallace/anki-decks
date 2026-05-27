---
id: "4bc6ab07adef4c438b2794cda2ceabb9"
tags: [syntax]
---

# Front
Define a generator

# Back
A function with `yield`, or a generator expression — an iterator whose values are computed on demand.

```python
def gen():
    yield 1
    yield 2

squares = (x*x for x in xs)
```

All iterators are lazy in *delivery* (one value per `next()`), but a generator is lazy in *computation* too — `iter([1,2,3])` is a cursor over an already-materialized list, whereas `(x*x for x in xs)` never builds the full sequence.
