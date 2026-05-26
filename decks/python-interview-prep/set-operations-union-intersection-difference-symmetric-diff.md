---
id: "fc404315aa694ce58f660b72972ae148"
tags: [set]
---

# Front
Set operations: union, intersection, difference, symmetric diff

# Back
For sets `a`, `b`:

| Operator | Meaning | Method form |
|----------|---------|-------------|
| `a \| b` | union (in either) | `a.union(b)` |
| `a & b` | intersection (in both) | `a.intersection(b)` |
| `a - b` | difference (in `a`, not `b`) | `a.difference(b)` |
| `a ^ b` | symmetric diff (in exactly one) | `a.symmetric_difference(b)` |

Operators require both sides to be sets; the **method forms accept any iterable** (`a.union([1, 2])`).

Build sets with `set(iterable)` (e.g. `set([1, 2, 3])`, `set("abc")`) or a literal `{1, 2, 3}`. Note `{}` is an empty **dict** — the empty set is `set()`.
