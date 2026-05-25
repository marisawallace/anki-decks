---
id: "3a890dba94264353878254e4da55b7d9"
tags: [sorting, footgun]
---

# Front
Multi-key sort with mixed directions (age desc, name asc)

# Back
Negate the numeric key: `key=lambda p: (-p.age, p.name)`. For non-numeric mixed order, sort twice (Python sort is stable): sort by minor key first, then major.
