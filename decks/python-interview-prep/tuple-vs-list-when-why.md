---
id: "d8b5e6c50b11489da46fb8302f4f83fa"
tags: [syntax, footgun]
---

# Front
Tuple vs list — when/why

# Back
Tuples are immutable & hashable (can be dict keys / set elements); lists are mutable. Single-element tuple needs a comma: `(1,)`.
