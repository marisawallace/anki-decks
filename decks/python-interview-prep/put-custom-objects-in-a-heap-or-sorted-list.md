---
id: "411ba38d3a6c433095d95d70d354b53e"
tags: [stdlib, sorting, slatkin]
---

# Front
Put custom objects in a heap or sorted list

# Back
`heapq`/`sorted` compare with `<`, so an arbitrary class raises `TypeError: '<' not supported`. Three fixes:

**1. `(priority, item)` tuples** — simplest, no class changes. Tuples compare left-to-right:
```python
import heapq
h = []
heapq.heappush(h, (2, "write tests"))
heapq.heappush(h, (1, "fix bug"))
heapq.heappop(h)  # (1, "fix bug")
```
Gotcha: if priorities tie, Python falls through to comparing `item`. If `item` isn't orderable (e.g. a custom class), this crashes. Add a tiebreaker:
```python
import itertools
counter = itertools.count()
heapq.heappush(h, (priority, next(counter), item))  # insertion order breaks ties
```

**2. `@dataclass(order=True)`** — auto-generates `__lt__` etc. from fields in declared order. Exclude fields you don't want to compare:
```python
from dataclasses import dataclass, field
@dataclass(order=True)
class Task:
    priority: int
    name: str = field(compare=False)
```

**3. Define `__lt__`** — only method `heapq`/`sorted` actually need:
```python
class Task:
    def __init__(self, priority, name):
        self.priority, self.name = priority, name
    def __lt__(self, other):
        return self.priority < other.priority
```

For `sorted`, a `key=` function is usually cleaner: `sorted(tasks, key=lambda t: t.priority)`. `heapq` has no `key=` parameter — that's why the tuple trick is so common.
