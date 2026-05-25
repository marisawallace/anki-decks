---
id: "0a31cb7ab40345b2a9f93a991dd8abe8"
tags: [string, ruby-diff]
---

# Front
Are Python strings mutable?

# Back
No — immutable. `s[0] = "x"` errors. Build new strings or use a `list(s)` then `"".join(...)`.
