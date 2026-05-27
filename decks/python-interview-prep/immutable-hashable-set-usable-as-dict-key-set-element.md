---
id: "fb48f3e770c14e4aaceba345e21f592f"
tags: [set]
---

# Front
Immutable, hashable set (usable as dict key / set element)

# Back
`frozenset([1, 2, 3])`.

A regular `set` is mutable, so it has no stable hash — Python refuses to use it as a dict key or put it inside another set. `frozenset` is the immutable counterpart: same operations (`|`, `&`, `-`, `in`), but hashable.

```python
seen = set()
seen.add(frozenset({1, 2}))      # ok
seen.add(frozenset({2, 1}))      # dedupes — same frozenset

cache[frozenset(args)] = result  # memoize on an unordered arg set
```

Reach for it when the *set itself* is a key/element: memoizing on unordered inputs, deduping groups (`{frozenset(team) for team in teams}`), or canonicalizing graph edges (`frozenset({u, v})`).
