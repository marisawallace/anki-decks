---
id: "ac6b38143406457989623126b7c4e482"
tags: [dict, comprehension]
---

# Front
Comprehension over a dict to invert it

# Back
`{v: k for k, v in d.items()}` (assumes values are unique & hashable).
