---
id: "57e3e4c20aab408986dca8593972c6a7"
---

# Front
Run code whenever a class is subclassed

# Back
Define `__init_subclass__(cls, **kwargs)` on the parent. Python calls it on the **subclass** at class-creation time. Covers most "register subclasses" / "enforce subclass shape" use cases without a metaclass.

```python
class Plugin:
    registry = {}
    def __init_subclass__(cls, *, name, **kw):
        super().__init_subclass__(**kw)
        cls.name = name
        Plugin.registry[name] = cls

class Csv(Plugin, name="csv"): ...
class Tsv(Plugin, name="tsv"): ...

Plugin.registry   # {'csv': Csv, 'tsv': Tsv}
```

Extra keyword args from the `class X(Base, name="csv"):` line flow in as `**kwargs`. Reach for this *before* writing a metaclass.
