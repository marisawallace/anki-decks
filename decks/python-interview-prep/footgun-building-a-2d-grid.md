---
id: "f9f8dd58bfb64c4ab14a53d46fdd56cd"
tags: [footgun, list]
---

# Front
Footgun: building a 2D grid

# Back
`[[0]*cols for _ in range(rows)]`. NOT `[[0]*cols]*rows` — that makes `rows` references to the SAME inner list.
