---
id: "bc1c7f7c0873454ab6f2ed375f23561b"
tags: [footgun, list]
---

# Front
Footgun: copying a list vs aliasing

# Back
`b = a` aliases (same object). Copy: `b = a[:]`, `b = list(a)`, or `b = a.copy()`. Nested: `import copy; copy.deepcopy(a)`.
