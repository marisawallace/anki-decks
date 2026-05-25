---
id: "80ee93c0ff244dd0988f77f2c4387ed8"
tags: [dict]
---

# Front
`setdefault`: what does it do?

# Back
`d.setdefault(k, []).append(x)` — returns `d[k]`, inserting `k: default` first if missing. One-liner for grouping — but Slatkin prefers `defaultdict` when repeatedly building internal state.
