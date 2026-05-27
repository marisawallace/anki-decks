---
id: "0810ece3796e4ea6bea5b1fe827f0b51"
tags: [ruby-diff, stdlib]
---

# Front
Reduce/fold a list (Ruby: `arr.reduce(:+)`)

# Back
`from functools import reduce; reduce(lambda a, b: a+b, arr, 0)`. For sums just use `sum(arr)`.

Filtered/transformed folds are idiomatically a generator expression fed to a builtin reducer (`sum`, `max`, `min`, `any`, `all`, `math.prod`, `"".join`):

```python
sum(x for x in arr if x % 2 == 0)   # sum of evens
max(len(s) for s in lines)
any(x < 0 for x in arr)             # short-circuits
```

Comprehensions themselves only map/filter — they produce a sequence, not a scalar. Wrap one in a reducer to fold.
