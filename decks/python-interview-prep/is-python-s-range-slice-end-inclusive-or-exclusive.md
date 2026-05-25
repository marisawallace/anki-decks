---
id: "5bbf55e7911b4640b850d7d5a40d59c9"
tags: [footgun, syntax]
---

# Front
Is Python's `range`/slice end inclusive or exclusive?

# Back
Exclusive. `range(0, 5)` → 0,1,2,3,4. `a[2:5]` excludes index 5.
