---
id: "f9339f4a346240bb8f7a4e9729880b0f"
tags: [footgun, ruby-diff]
---

# Front
Equality vs identity: `==` vs `is`

# Back
`==` compares values; `is` compares object identity. Use `is` only for `None`/`True`/`False` singletons.
