---
id: "d238f39865ef4f8697e9433e15bd41e3"
tags: [dict, stdlib]
---

# Front
`defaultdict` for auto-initializing values

# Back
`from collections import defaultdict; d = defaultdict(list); d[k].append(x)`. Missing keys auto-create via the factory (`int`→0, `list`→[], `set`→set()). Slatkin: prefer over `setdefault` for building state — `setdefault` constructs the default on every call, even on hits.
