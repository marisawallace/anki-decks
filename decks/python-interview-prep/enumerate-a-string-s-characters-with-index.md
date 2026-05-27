---
id: "e26d85b2a246438cb6d5c47ccda40316"
tags: [string, syntax]
---

# Front
Enumerate a string's characters with index

# Back
`for i, ch in enumerate(s):` — strings are iterable sequences of 1-char strings.

Analogues:
- list: `for i, x in enumerate(lst):`
- dict: `for i, (k, v) in enumerate(d.items()):` (or `enumerate(d)` for just keys)
- start at 1: `enumerate(xs, start=1)`
