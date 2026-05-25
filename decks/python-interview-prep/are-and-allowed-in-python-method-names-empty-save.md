---
id: "e60f1279d3f24524a6b51cd021fe7da1"
tags: [ruby-diff]
---

# Front
Are `?` and `!` allowed in Python method names? (`empty?`, `save!`)

# Back
No. Identifiers are `[A-Za-z_][A-Za-z0-9_]*`. Convention: `is_empty()`, and trailing `_` to avoid keywords (`class_`).
