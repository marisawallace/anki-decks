---
id: "a585dd9db81a4d5daeb6df5ab4c0b6b8"
tags: [syntax]
---

# Front
Unpack with a catch-all (Ruby splat `a, *rest = arr`)

# Back
`first, *rest = [1,2,3,4]` → `first=1, rest=[2,3,4]`. Also `*init, last = ...`.
