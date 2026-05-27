---
id: "5a9a98bbe3f2443cb24cdeab51dd966b"
tags: [stdlib, string]
---

# Front
Ascii lowercase/uppercase/digits constants

# Back
`import string; string.ascii_lowercase` → `'abc...xyz'`, `.ascii_uppercase` → `'ABC...XYZ'`, `.digits` → `'0123456789'`. Also `.ascii_letters`, `.hexdigits`, `.punctuation`, `.whitespace`.

Use these when you need the alphabet **as data** — to iterate, index into, build a lookup, or sample from:

```python
shift = {c: string.ascii_lowercase[(i+3)%26] for i, c in enumerate(string.ascii_lowercase)}
''.join(random.choices(string.ascii_letters + string.digits, k=8))
```

Use `str.lower()` / `str.upper()` / `str.isdigit()` when you have a string and want to **transform or test** it. They're not interchangeable: the constants give you the alphabet itself; the methods operate on a string you already have.

Also note `c.isalpha()` / `c.isdigit()` are Unicode-aware (match `é`, `٤`), whereas `c in string.ascii_letters` is strict ASCII — pick deliberately.
