---
id: "04aadb244783495a94a4e82313aab481"
tags: [syntax, footgun]
---

# Front
`global` vs `nonlocal`

# Back
`global x` rebinds a module-level var inside a function; `nonlocal x` rebinds an enclosing (outer function) var.
