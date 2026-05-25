---
id: "d50206d7a2934b7ab01ec6ad8f732a28"
tags: [ruby-diff, footgun]
---

# Front
Does Python auto-return the last expression? (Ruby does)

# Back
No. You must write `return` explicitly; functions without it return `None`.
