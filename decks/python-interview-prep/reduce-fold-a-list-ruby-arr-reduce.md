---
id: "0810ece3796e4ea6bea5b1fe827f0b51"
tags: [ruby-diff, stdlib]
---

# Front
Reduce/fold a list (Ruby: `arr.reduce(:+)`)

# Back
`from functools import reduce; reduce(lambda a, b: a+b, arr, 0)`. For sums just use `sum(arr)`.
