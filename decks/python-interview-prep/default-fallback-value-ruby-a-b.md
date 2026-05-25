---
id: "13a6bfafb8d24281a0652fde0c124420"
tags: [ruby-diff, footgun]
---

# Front
Default/fallback value (Ruby: `a || b`)

# Back
`a or b` returns `a` if truthy else `b`. Careful: treats `0`/`""`/`[]` as fallback-triggering (use `a if a is not None else b` to only catch None).
