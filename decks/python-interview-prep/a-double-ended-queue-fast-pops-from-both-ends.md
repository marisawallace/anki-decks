---
id: "ee4ba2fada2e4bc08af3a10c57844a86"
tags: [stdlib]
---

# Front
A double-ended queue (fast pops from both ends). How and why would you use this for BFS?

# Back
`from collections import deque; q = deque(); q.append(x); q.popleft()`. O(1) both ends — use for BFS.

```python
from collections import deque

def bfs(graph, start):
    seen = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for nbr in graph[node]:
            if nbr not in seen:
                seen.add(nbr)
                q.append(nbr)
    return seen
```
