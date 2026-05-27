---
id: "f9339f4a346240bb8f7a4e9729880b0f"
tags: [footgun, ruby-diff]
---

# Front
Equality vs identity: `==` vs `is`

# Back
`==` compares values (calls `__eq__`); `is` compares object identity (same object in memory). Use `is` when you mean "same object" — `None`/`True`/`False` singletons, sentinel objects (`_MISSING = object()`), enum members, cycle detection. Never use `==` with `None` (`__eq__` can be overridden).
