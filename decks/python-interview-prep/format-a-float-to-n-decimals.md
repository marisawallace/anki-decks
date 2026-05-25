---
id: "6f2e7585a2b24440ab7b8fff383366b5"
tags: [string, footgun]
---

# Front
Format a float to N decimals

# Back
`f"{x:.2f}"` or `round(x, 2)` (note `round` does banker's rounding: `round(0.5)`→0).
