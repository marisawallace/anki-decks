---
id: "7e66080a423e4379b30302c81e89526b"
---

# Front
Computed/validated attribute that looks like a field

# Back
`@property` for the getter, `@<name>.setter` for the setter. Call sites stay as plain attribute access — no parens.

```python
class Temperature:
    def __init__(self, c): self.celsius = c   # goes through setter

    @property
    def celsius(self):
        return self._c

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._c = value

    @property
    def fahrenheit(self):        # read-only computed view
        return self._c * 9/5 + 32
```

This is why Python doesn't use `get_x` / `set_x` conventions — start with a plain attribute, switch to `@property` later without changing any caller.
