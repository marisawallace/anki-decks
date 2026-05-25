---
id: "7588edb4f45d493cb527f67995134cd0"
tags: [sorting, stdlib, slatkin]
---

# Front
Sort by a custom pairwise comparator

# Back
Python 3 has no `cmp=`. `from functools import cmp_to_key; sorted(xs, key=cmp_to_key(cmp))` where `cmp(a, b)` returns negative / 0 / positive. Prefer a plain `key=` when expressible.
