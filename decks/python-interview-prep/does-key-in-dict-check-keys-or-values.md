---
id: "2c3d334344d24c61a8c58c4c0710c1bc"
tags: [dict, footgun]
---

# Front
Does `key in dict` check keys or values?

# Back
Keys only. To check values: `val in d.values()` (O(n)).
