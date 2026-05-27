---
id: "804b68b673c045d289f94c5d7db6693b"
tags: [stdlib]
---

# Front
Memoize a recursive function

# Back
```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

`@cache` (3.9+) = `@lru_cache(maxsize=None)`, unbounded. Use `@lru_cache(maxsize=128)` for an LRU eviction policy.

**Under the hood:** wraps the function in a closure holding a `dict` keyed by `(args, tuple(sorted(kwargs.items())))`. On call, builds the key, looks it up, returns hit or computes+stores. `lru_cache` uses a doubly-linked list + dict to track recency.

**Gotchas:**
- **All args must be hashable** — passing a `list`/`dict`/`set` raises `TypeError: unhashable type`. Convert to `tuple`/`frozenset` at the call site.
- `f(1, 2)` and `f(1, y=2)` are cached as *different* keys (different kwargs shape).
- **Cache lives on the function object** — module-level `@cache` persists for the process lifetime → memory leak risk for long-running services. Inspect with `f.cache_info()`, clear with `f.cache_clear()`.
- **Methods:** `@cache` on a method keys on `self`, which keeps the instance alive (cache holds a strong ref) — leaks instances. Prefer `functools.cached_property` for per-instance memoization, or use `weakref`.
- Not thread-safe for the *function body* (two threads can both miss and compute), but the dict update itself is fine under the GIL.
- Decorating a recursive function: the recursive call must resolve to the *decorated* version, or recursion bypasses the cache. The `@` syntax handles this — recursive calls look up `fib` in the enclosing scope at call time, finding the wrapped version:
    ```python
    @cache
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)  # `fib` here = wrapped
    ```
    Manual rebinding works the same way (decorator syntax desugars to this):
    ```python
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    fib = cache(fib)   # name `fib` now points to wrapped; recursion hits it
    ```
    But this **breaks** — recursion still calls the *original*, so only the outermost call is cached:
    ```python
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    cached_fib = cache(fib)   # original `fib` still bound; recursive lookups skip the cache
    cached_fib(30)            # 2^30 calls, not 30
    ```

**Roll your own:**
```python
def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper
```
Skips kwargs, no eviction, no stats — but captures the essence: closure + dict + key from args.
