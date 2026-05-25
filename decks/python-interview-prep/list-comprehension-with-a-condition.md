---
id: "157dfc70f981460390beb04f486bdf90"
tags: [comprehension, footgun]
---

# Front
List comprehension with a condition

# Back
Filter: `[x for x in xs if x > 0]`. Conditional value: `[x if x > 0 else 0 for x in xs]` (note position differs!).
