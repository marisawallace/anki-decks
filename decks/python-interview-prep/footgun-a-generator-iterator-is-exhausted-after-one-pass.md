---
id: "16401a8224e64faeb58b5129cb93265a"
tags: [footgun, generator, slatkin]
---

# Front
Footgun: a generator/iterator is exhausted after one pass

# Back
`g = (x for x in xs)` — a second `for`/`sum` over `g` sees nothing. Materialize with `list(g)` to reuse, or write functions that take a container, not a bare iterator.

## `(...)` vs `[...]` — generator expression vs list comprehension

The syntax looks parallel, but the results are very different:

```python
g = (x*x for x in xs)   # generator expression → generator object (lazy, one-shot)
L = [x*x for x in xs]   # list comprehension   → list                (eager, reusable)
```

Both desugar to roughly the same loop; the brackets pick the **collection strategy**:

- `[...]` runs the loop to completion and returns a `list`.
- `(...)` builds a generator — nothing runs until you iterate it. Each `next()` resumes the frame, yields one value, and suspends. When the source is exhausted, `StopIteration` is raised and the generator is dead. Re-iterating gives you zero items, not a fresh pass.

So `list(g)` and `[x*x for x in xs]` produce equal lists, but the comprehension is a single eager expression while `list(g)` drains a generator you happen to have.

## Do comprehensions ever return an iterator?

The three "comprehension" forms always return a concrete container — never a lazy iterator:

| Syntax              | Returns       |
|---------------------|---------------|
| `[x for x in xs]`   | `list`        |
| `{x for x in xs}`   | `set`         |
| `{k: v for ...}`    | `dict`        |
| `(x for x in xs)`   | **generator** (this one is *not* a comprehension; it's a generator expression) |

Rule of thumb: square/curly brackets → eager container; parentheses → lazy generator. If you want laziness, use `(...)` or a `def`-with-`yield` function; if you want to iterate twice, use `[...]` (or call `list()` on the generator).
