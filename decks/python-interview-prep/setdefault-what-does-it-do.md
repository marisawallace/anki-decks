---
id: "80ee93c0ff244dd0988f77f2c4387ed8"
tags: [dict]
---

# Front
`setdefault`: what does it do?

# Back
`d.setdefault(k, default)` looks up `k` in `d`:

- if `k` **is present**, it returns the existing `d[k]` (the `default` is ignored — `d` is unchanged).
- if `k` **is missing**, it first does `d[k] = default`, then returns that `default`.

Either way you get back the value now stored at `k`, so you can mutate it in place:

```python
d.setdefault(k, []).append(x)
```

On the first `x` for a key this inserts `k: []` then appends; on later ones it grabs the existing list and appends. Result: a one-liner for grouping items into lists.

**Caveat:** the `default` is built on *every* call, even when `k` already exists — so `setdefault(k, [])` allocates a throwaway list each time. For repeatedly building up internal state, Slatkin (*Effective Python*) prefers `defaultdict(list)`, which only constructs the default when it's actually needed.
