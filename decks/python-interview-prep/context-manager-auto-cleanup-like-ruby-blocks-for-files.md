---
id: "d5b6472e4b934b51bb1fb3eeb0725b94"
tags: [syntax]
---

# Front
Context manager (auto-cleanup, like Ruby blocks for files)

# Back
`with open("f") as fh:` — guarantees close on exit, even on exception.
