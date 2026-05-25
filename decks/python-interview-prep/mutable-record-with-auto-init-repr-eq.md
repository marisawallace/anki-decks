---
id: "1307922328a64e61969192ce6321260f"
tags: [stdlib, slatkin, record]
---

# Front
Mutable record with auto __init__/__repr__/__eq__

# Back
`from dataclasses import dataclass`, then `@dataclass`
`class Node:`
`    val: int`
`    next: "Node" = None`. Add `@dataclass(order=True)` to also get comparison methods.
