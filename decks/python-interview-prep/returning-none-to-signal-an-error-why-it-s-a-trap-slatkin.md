---
id: "a46b429b0ecf43368742c2827691631e"
tags: [slatkin, footgun]
---

# Front
Returning None to signal an error — why it's a trap (Slatkin)

# Back
A caller's `if not result:` can't tell None (error) from a valid `0`/`""`/`[]`. Prefer `raise ValueError(...)` over returning None.
