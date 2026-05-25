---
id: "a935a358736a420c80ceec234ab3fd96"
tags: [comprehension, stdlib]
---

# Front
Count items matching a condition

# Back
`sum(1 for x in xs if cond(x))` — sum of a generator of 1s. (`sum(cond(x) for x in xs)` since bools are ints.)
