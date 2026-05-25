---
id: "19c04e3bb1c34594af1a48515c114903"
tags: [syntax]
---

# Front
try/except/else/finally structure

# Back
```python
try:
    risky()
except ValueError as e:
    handle(e)
else:
    ran_if_no_error()
finally:
    always()
```
