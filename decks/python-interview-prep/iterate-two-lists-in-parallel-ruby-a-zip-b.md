---
id: "753cd3d59f814da1a9f610db827b6846"
tags: [list, stdlib]
---

# Front
Iterate two lists in parallel (Ruby: `a.zip(b)`)

# Back
`for x, y in zip(a, b):`. Stops at the shorter; `import itertools; itertools.zip_longest(a, b)` to pad.
