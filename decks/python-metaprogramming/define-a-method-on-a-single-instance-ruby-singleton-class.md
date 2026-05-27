---
id: "32bf3ae2fe5e4bfab171f58ae8d11eb7"
---

# Front
Add a method to one instance only — Ruby's singleton class / `def obj.foo`

# Back
Python has no per-instance method dispatch. Plain assignment stores the function as an ordinary attribute — it is **not** bound, so `self` is not passed:

```python
class Dog: pass
d = Dog()
d.bark = lambda self: "woof"
d.bark()        # TypeError: missing 'self'
d.bark(d)       # works, but ugly
```

Bind it explicitly with `types.MethodType`:

```python
import types
d.bark = types.MethodType(lambda self: "woof", d)
d.bark()        # 'woof'
```

Only `d` gets the method; other `Dog()`s don't. Usually a code smell in Python — prefer a subclass or composition.
