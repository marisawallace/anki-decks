---
id: "e35bd93a751c472c8efff7d47e484f35"
tags: [ruby-diff, string]
---

# Front
String interpolation in Python

# Back
**f-strings**: prefix a literal with `f` and embed any expression in `{...}`:

**Format specs** go after a `:` inside the braces (`{value:spec}`):
- `f"{x:.2f}"` → fixed 2 decimals (`3.14`)
- `f"{x:>5}"` / `f"{x:<5}"` / `f"{x:^5}"` → right/left/center pad to width 5
- `f"{x:,}"` → thousands separator (`1,000,000`)

**Debug form** `f"{x=}"` (3.8+) prints `x=<value>` — note the `=` sits right after the expression, not inside the spec. Great for quick logging.

Escape literal braces by doubling: `f"{{}}"` → `{}`.