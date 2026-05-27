---
id: "f9502edc1a1742b2aab929fcbf048168"
---

# Front
Decorators — how to create and use

# Back
A decorator is a function that takes a function and returns a (usually wrapped) function. `@deco` above `def f` is sugar for `f = deco(f)`.

```python
from functools import wraps

def log_calls(fn):
    @wraps(fn)                       # preserve __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        result = fn(*args, **kwargs)
        print(f"-> {result!r}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)   # prints "calling add" then "-> 5"
```

Decorator **with arguments** = a function that returns a decorator (three nested layers):

```python
def repeat(n):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return deco

@repeat(3)
def greet(name): print(f"hi {name}")
```

Notes:
- Always use `@wraps(fn)` so introspection and tracebacks point at the original.
- Decorators run **at definition time**, top-down in source but applied bottom-up: `@a` / `@b` / `def f` → `f = a(b(f))`.
- Common uses: logging, timing, caching (`functools.lru_cache`), auth checks, registering handlers.
