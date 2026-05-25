---
id: "9ad06fdef4854278b58c20c604ebcb4f"
tags: [stdlib, itertools, footgun]
---

# Front
Group consecutive equal items

# Back
`from itertools import groupby; for key, grp in groupby(sorted(xs)):` — `grp` is an iterator. GOTCHA: only groups *adjacent* equal items, so sort by the same key first.
