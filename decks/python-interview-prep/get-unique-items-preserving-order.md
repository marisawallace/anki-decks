---
id: "0b346597e4e64054aebd3aa61c185bd1"
tags: [dict, footgun]
---

# Front
Get unique items preserving order

# Back
`list(dict.fromkeys(items))` — dedupes, keeps first-seen order. `set(items)` dedupes but loses order.
