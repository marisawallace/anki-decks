---
id: "a732562e951c4415b44b805c657ee040"
tags: [footgun, syntax]
---

# Front
Initialize multiple variables to the same value

# Back
`a = b = c = 0` (fine for immutables). Don't do this with a mutable like `[]` — all alias the same object.
