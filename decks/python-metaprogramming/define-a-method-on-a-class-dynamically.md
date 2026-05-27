---
id: "591cee7a18ed4d549df3b5039c7bf6e8"
---

# Front
Add a method to a class at runtime

# Back
Assign a function to the class. Functions stored on a class auto-bind as methods on instances (the descriptor protocol does the work):

```python
class Dog: pass

def bark(self, n=1):
    return "woof " * n

Dog.bark = bark                  # or: setattr(Dog, "bark", bark)
Dog().bark(3)                    # 'woof woof woof '
```

Already-created instances see the new method too (lookup goes through the class). This is how monkey-patching works in Python — and why it usually only works on classes *you* define (most C-implemented builtins like `list`, `dict`, `str` reject attribute assignment).
