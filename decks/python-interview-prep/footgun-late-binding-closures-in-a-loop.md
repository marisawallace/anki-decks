---
id: "0901baa0cdc14a2891d7a6e46b919f2b"
tags: [footgun]
---

# Front
Footgun: late-binding closures in a loop

# Back
`[lambda: i for i in range(3)]` all return 2. Capture now: `lambda i=i: i`.
