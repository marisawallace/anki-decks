---
id: "ff7da75c882a4090b7456cad6d9d4057"
---

# Front
Descriptors — how `@property`, methods, and `classmethod` work underneath

# Back
A **descriptor** is any object whose class defines `__get__` (and optionally `__set__`/`__delete__`). When stored on a class, Python invokes the descriptor on attribute access instead of returning it raw. That's why `def foo(self)` becomes a bound method on instances — **functions are descriptors**.

```python
class Typed:
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return obj.__dict__[self.name]
    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be int")
        obj.__dict__[self.name] = value

class Point:
    x = Typed()
    y = Typed()

p = Point(); p.x = 3        # ok
p.x = "oops"                # TypeError
```

Descriptors live on the **class**, not the instance — that's the rule that makes them fire.
