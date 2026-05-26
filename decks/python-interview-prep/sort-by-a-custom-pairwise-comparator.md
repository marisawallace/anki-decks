---
id: "7588edb4f45d493cb527f67995134cd0"
tags: [sorting, stdlib, slatkin]
---

# Front
Sort by a custom pairwise comparator

# Back
Wrap a two-argument comparator with `cmp_to_key`. The comparator is **yours to define** (`cmp` is not a builtin — calling it without defining it is a `NameError`):

```python
from functools import cmp_to_key

def cmp(a, b):                 # negative: a first | 0: equal | positive: b first
    if a % 2 != b % 2:
        return -1 if a % 2 == 0 else 1   # evens before odds
    return a - b                          # otherwise ascending

sorted([5, 2, 8, 1, 3], key=cmp_to_key(cmp))   # [2, 8, 1, 3, 5]
```

The sign convention matches C's `qsort` / Java's `Comparator`.

**How it works:** `key=` must be a *callable*; the sort calls `key(x)` per element and then compares the returned keys using **`<` (`__lt__`) only**. `cmp_to_key(cmp)` returns a **class** whose instances implement `__lt__` (and friends) by calling your `cmp`:

```python
def cmp_to_key(mycmp):
    class K:
        def __init__(self, obj): self.obj = obj
        def __lt__(self, other): return mycmp(self.obj, other.obj) < 0
        # __gt__/__eq__/... too, but sort only ever uses __lt__
    return K
```

So `K(a) < K(b)` runs `cmp(a, b) < 0` — the bridge from a pairwise comparator back to the single-key, `<`-only model sort requires.

**Prefer a plain `key=`** when order is a derived per-element value: clearer and faster (*O(n)* key calls vs *O(n log n)* comparator calls). Use `cmp_to_key` only when order is genuinely pairwise, e.g. "largest number" — arrange ints into the biggest concatenation by ordering strings `a`, `b` on `a+b` vs `b+a`:

```python
def cmp(a, b):
    if a + b > b + a: return -1
    if a + b < b + a: return 1
    return 0
"".join(sorted(map(str, [3,30,34,5,9]), key=cmp_to_key(cmp)))   # "9534330"
```
