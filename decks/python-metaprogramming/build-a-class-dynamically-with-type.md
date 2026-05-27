---
id: "67e1ad39c57b47918206e32f0ca1c03c"
---

# Front
Build a class at runtime

# Back
Call `type` with three args: `type(name, bases, namespace)`. The result is exactly what a `class` statement would have produced.

```python
def greet(self):
    return f"hi, I'm {self.name}"

Point = type(
    "Point",
    (object,),
    {"name": "p", "greet": greet},
)

Point().greet()    # "hi, I'm p"
```

Equivalent to:

```python
class Point:
    name = "p"
    def greet(self): ...
```

Useful for ORMs, plugin systems, and anywhere the set of classes is only known at runtime. (One-arg `type(x)` is the unrelated "what's its class?" call.)
