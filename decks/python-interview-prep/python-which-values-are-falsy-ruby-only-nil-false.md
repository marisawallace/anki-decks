---
id: "734720684aab4b94b9ec80b4a2382713"
tags: [ruby-diff, footgun]
---

# Front
Python: which values are falsy? (Ruby: only `nil`/`false`)

# Back
`False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `()`, and any empty collection. Everything else is truthy.
