---
id: "3e51fc8b5416475aa0e0209d86f116b0"
tags: [footgun]
---

# Front
Footgun: modifying a list/dict while iterating it

# Back
Don't. Iterate a copy (`for x in list(d):`) or build a new collection.
