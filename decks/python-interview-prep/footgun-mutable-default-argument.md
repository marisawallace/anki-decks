---
id: "f7f44939a6a84b95a22714b4dbbc0a42"
tags: [footgun]
---

# Front
Footgun: mutable default argument

# Back
`def f(x, acc=[])` reuses the SAME list across calls. Use `def f(x, acc=None):` then `if acc is None: acc = []` — NOT `acc = acc or []`, which discards a legitimately-passed empty list.
