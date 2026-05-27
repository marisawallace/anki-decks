---
id: "9ad06fdef4854278b58c20c604ebcb4f"
tags: [stdlib, itertools, footgun]
---

# Front
Group consecutive equal items

# Back
```python
from itertools import groupby
for key, grp in groupby(sorted(xs)):
    print(key, list(grp))

# with a key function (e.g. group words by length):
for k, grp in groupby(sorted(words, key=len), key=len):
    ...
```

**Footguns:**
- Only groups **adjacent** equal items — almost always sort by the same key first (Unix `uniq` has the same quirk).
- `grp` is a **one-shot iterator** tied to the underlying sequence. Advancing the outer loop **invalidates** the previous `grp`. So `[(k, g) for k, g in groupby(xs)]` gives empty groups — materialize with `list(g)` *before* the next iteration: `[(k, list(g)) for k, g in groupby(xs)]`.
- Keys are compared with `==`, not hashed — items don't need to be hashable, just comparable. `sorted` does require an ordering though.
- `NaN` breaks it (NaN != NaN), as does mixing types that don't compare.

**Under the hood:** roughly a generator that walks the input once, keeps the current key, and yields a sub-iterator that pulls from the same source until the key changes. That shared source is why `grp` expires.

**Roll your own:**
```python
def groupby(xs, key=lambda x: x):
    it = iter(xs)
    try:
        x = next(it)
    except StopIteration:
        return
    cur = key(x)
    group = [x]
    for x in it:
        k = key(x)
        if k == cur:
            group.append(x)
        else:
            yield cur, group
            cur, group = k, [x]
    yield cur, group
```
(Stdlib version yields a lazy iterator instead of a list — more memory-efficient but introduces the invalidation footgun above.)
