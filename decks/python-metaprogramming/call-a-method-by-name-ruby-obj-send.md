---
id: "e42832fe040b4d828cba8c467ed96689"
---

# Front
Call a method by name — Ruby's `obj.send(:foo, x)`

# Back
Use `getattr` — methods are just attributes that happen to be callable.

```python
getattr(obj, "foo")(x)              # raises AttributeError if missing
getattr(obj, "foo", None)           # safe lookup; None if missing
fn = getattr(obj, "foo", None)
if callable(fn):
    fn(x)
```

Works for any attribute, not just methods. The name can be built at runtime — useful for dispatch tables, plugin systems, and REPL/CLI command routing.
