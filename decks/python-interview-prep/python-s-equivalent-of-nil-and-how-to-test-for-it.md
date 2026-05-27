---
id: "4a6d6ddd742a47f7aae6aa900967d640"
tags: [ruby-diff, syntax]
---

# Front
Python's equivalent of `nil`, and how to test for it

# Back
`None`. Test identity with `x is None` / `x is not None` (not `== None`).

`None` is a singleton, so identity (`is`) is the correct check and is faster. `==` calls `__eq__`, which a class can override to return `True` for non-`None` values (e.g. NumPy arrays raise or return an array, pandas `NaT`/`NA` return weird truthiness) — so `x == None` can lie or blow up. PEP 8 mandates `is None`.
