---
id: "a6e3cb6c817141d9a4ddfbb291ad6980"
tags: [stdlib]
---

# Front
Generate permutations / combinations / cartesian product

# Back
`from itertools import permutations, combinations, combinations_with_replacement, product`

All take **any iterable** (list, tuple, str, set, generator, range, ...) and return an **iterator of tuples**. Wrap in `list(...)` to materialize.

```python
permutations('ABC', 2)
# AB AC BA BC CA CB     — order matters, no repeats

combinations('ABC', 2)
# AB AC BC              — order doesn't matter, no repeats (input order preserved)

combinations_with_replacement('ABC', 2)
# AA AB AC BB BC CC

product([1, 2], ['a', 'b'])
# (1,'a') (1,'b') (2,'a') (2,'b')   — cartesian product of N iterables

product([0, 1], repeat=3)
# all 8 binary triples: (0,0,0) (0,0,1) ... (1,1,1)
```

Notes:
- `permutations(xs)` with no `r` defaults to `r=len(xs)` (full-length perms).
- "No repeats" means **by position**, not by value: `permutations('AAB', 2)` still yields 6 tuples.
- A generator argument is consumed once internally and buffered — fine, but you can't re-use it.
- All are lazy; safe on large inputs as long as you don't `list()` them.
