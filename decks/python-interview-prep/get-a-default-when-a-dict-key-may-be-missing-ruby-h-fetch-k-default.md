---
id: "7cea601a6cf74878811637f3d6717107"
tags: [dict, footgun]
---

# Front
Get a default when a dict key may be missing

# Back
`d.get(k, default)` — returns `default` (or `None`) instead of raising. `d[k]` raises `KeyError`.
