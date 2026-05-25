---
id: "16401a8224e64faeb58b5129cb93265a"
tags: [footgun, generator, slatkin]
---

# Front
Footgun: a generator/iterator is exhausted after one pass

# Back
`g = (x for x in xs)` — a second `for`/`sum` over `g` sees nothing. Materialize with `list(g)` to reuse, or write functions that take a container, not a bare iterator.
