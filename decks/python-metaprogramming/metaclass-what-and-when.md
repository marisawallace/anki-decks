---
id: "a1fec125dfe34f2bbb50705c29a6da57"
---

# Front
What's a metaclass, and when do you actually need one?

# Back
A class is an instance of its **metaclass** (default `type`). `class C(metaclass=Meta): ...` calls `Meta(name, bases, namespace)` to build the class object itself. Override `__new__` / `__init__` to inspect or rewrite the class before it exists:

```python
class Upper(type):
    def __new__(mcs, name, bases, ns):
        ns = {k.upper() if not k.startswith("_") else k: v
              for k, v in ns.items()}
        return super().__new__(mcs, name, bases, ns)

class C(metaclass=Upper):
    def hello(self): return "hi"

C().HELLO()    # 'hi'   — note: hello got renamed
```

**Usually overkill.** Try first: `__init_subclass__`, class decorators, descriptors. Real metaclass uses: ABCs (`abc.ABCMeta`), ORMs (Django models), enforcing invariants across an entire hierarchy. Ruby roughly equivalent: a class's singleton class.
