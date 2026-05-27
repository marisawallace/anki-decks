---
id: "c773bdf5ad1d436c93453d83a7547352"
---

# Front
Reflect on an object's attributes by name

# Back
```python
getattr(obj, "x")            # AttributeError if missing
getattr(obj, "x", default)   # default if missing — preferred
setattr(obj, "x", value)     # obj.x = value, but name as string
hasattr(obj, "x")            # truthy iff getattr doesn't raise
delattr(obj, "x")            # del obj.x

vars(obj)                    # obj.__dict__ (instance attrs only)
dir(obj)                     # names visible on obj, incl. inherited
```

The first four are the reflection workhorses — useful whenever the attribute name is built at runtime (config keys, CLI flags, serializers). `hasattr` is just `getattr` + try/except, so use `getattr(obj, name, default)` directly when you also need the value.
