---
id: "032b0377ee4a470d989d004470a90ced"
tags: [string, comprehension]
---

# Front
String → list of ints (parse a line of numbers)

# Back
`[int(x) for x in line.split()]` or `list(map(int, line.split()))`. Raises `ValueError`.
