---
id: "04aadb244783495a94a4e82313aab481"
tags: [syntax, footgun]
---

# Front
`global` vs `nonlocal`

# Back
By default, assigning to a name inside a function creates a **new local** — even if a same-named variable exists outside. `global` and `nonlocal` opt out of that, telling Python "this name refers to a variable defined elsewhere; rebind *that* one."

- `global x` — `x` lives at **module scope**. Reads of an outer name work without `global`; you only need it to *rebind* (assign to) the module-level name from inside a function.
- `nonlocal x` — `x` lives in the **nearest enclosing function scope** (not module, not builtins). Used in closures to mutate a variable captured from an outer function.

```python
count = 0                  # module scope

def bump():
    global count
    count += 1             # rebinds the module-level `count`

def make_counter():
    n = 0                  # enclosing function scope
    def inc():
        nonlocal n
        n += 1             # rebinds `n` in make_counter, not a new local
        return n
    return inc
```

Without the declaration, `count += 1` / `n += 1` raises `UnboundLocalError` — Python sees the assignment, marks the name local, then fails the read.

Gotchas:
- `nonlocal` will **not** reach module scope — use `global` for that.
- Mutating a mutable object (`lst.append(...)`, `d[k] = v`) needs neither keyword; only **rebinding** the name does.

**Most closures don't need `nonlocal`** — you only hit it when rebinding an immutable captured name (a counter/accumulator). Cases that work without it:

- **Read-only capture** (decorators, callbacks, partial application):
  ```python
  def multiplier(factor):
      def mul(x): return x * factor   # reading only
      return mul
  ```
- **Mutating a captured container** (the pre-3.0 idiom, still common):
  ```python
  def memoize(fn):
      cache = {}
      def wrapper(*args):
          if args not in cache:
              cache[args] = fn(*args)  # mutating, not rebinding
          return cache[args]
      return wrapper
  ```
- **`self.attr = ...` in methods** — attribute assignment, not a local rebind.
