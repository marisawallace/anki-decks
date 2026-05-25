---
id: "de5aa134ad244cd6a4f315d31b06eabd"
tags: [ruby-diff, syntax]
---

# Front
Instantiate a class `Foo` (Ruby: `Foo.new`, JS: `new Foo()`)

# Back
`Foo()` — no `new`, no `.new`. `__init__` is the constructor.
