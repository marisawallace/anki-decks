---
id: "73076a87be234b0c927f6433e44d4099"
tags: [ruby-diff, comprehension]
---

# Front
Filter a list (Ruby: `arr.select { ... }`)

# Back
`[x for x in arr if cond(x)]` — Slatkin: prefer this. Reach for `list(filter(pred, arr))` only with an existing named predicate.
