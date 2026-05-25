---
id: "dc801a91c2c9461fab274b046544e26c"
tags: [set, footgun]
---

# Front
Create a set literal, and the empty-set gotcha

# Back
`{1, 2, 3}` is a set; but `{}` is an empty **dict**. Empty set is `set()`.
