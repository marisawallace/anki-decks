---
id: "b5944430a7794b0aa0cc5f31c10ea240"
---

# Front
Intercept missing attribute access — Ruby's `method_missing`

# Back
Define `__getattr__(self, name)` — it fires **only** when normal attribute lookup fails. Return a value or a callable; raise `AttributeError` to say "I don't handle that either".

```python
class Proxy:
    def __init__(self, target): self._t = target
    def __getattr__(self, name):
        # called only for attrs not found the normal way
        print(f"forwarding {name}")
        return getattr(self._t, name)

Proxy([1, 2, 3]).append(4)   # prints "forwarding append"
```

Contrast with `__getattribute__`, which fires on **every** access (including `self._t`) — trivial to recurse infinitely. Reach for `__getattr__` 99% of the time.
