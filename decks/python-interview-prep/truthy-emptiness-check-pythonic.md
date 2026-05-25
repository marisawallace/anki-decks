---
id: "463476bf2e544e0b9d88b0df12a45436"
tags: [ruby-diff, syntax]
---

# Front
Truthy emptiness check (Pythonic)

# Back
`if not lst:` for empty list/str/dict (relies on falsy empties). Prefer over `len(lst) == 0`.
