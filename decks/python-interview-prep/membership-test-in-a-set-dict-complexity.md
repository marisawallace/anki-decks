---
id: "a4c0e66719e8484496b16d0f0425ad70"
tags: [set, footgun]
---

# Front
Membership test in a set/dict — complexity?

# Back
`x in s` — average O(1) for set/dict (hashing). For a list it's O(n).
