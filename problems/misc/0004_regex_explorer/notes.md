---
platform: misc
problem_id: "0004"
slug: regex_explorer
difficulty: null
difficulty_rating: easy
language: [python]
topics: [string_ops]
date_solved: 2026-06-14
revisit: false
---

# Notes

## `re.compile()` -- Compile Once, Call on the Pattern Object

The `re` module has two ways to use a pattern. The first passes the pattern string
directly to module-level functions on every call:

```python
import re

re.findall(r"[^\w\s]", text)   # pattern compiled fresh each time
re.finditer(r"[^\w\s]", text)
```

The second compiles the pattern once into a pattern object, then calls methods on
that object:

```python
_SPECIAL = re.compile(r"[^\w\s]")

_SPECIAL.findall(text)    # reuses the compiled pattern
_SPECIAL.finditer(text)
```

The compiled version is more efficient when the same pattern is used multiple times
(e.g. called in a loop or across two methods). It also makes the pattern a named
constant, which improves readability -- `_SPECIAL.findall(text)` is clearer than
`re.findall(r"[^\w\s]", text)` scattered across the codebase.

In this problem, `_SPECIAL` is shared between `special_chars_pos()` and
`char_counts()`, so compiling at module level eliminates the duplication.

---

## Match Objects -- `.group()` and `.start()`

`re.finditer()` returns an iterator of match objects. Each match object carries
information about what was matched and where.

### `.group()`

Returns the actual matched string:

```python
import re

for m in re.finditer(r"[^\w\s]", "C++ is #1!"):
    print(m.group())   # "+", "+", "#", "!"
```

Calling `.group()` with no argument (or `.group(0)`) returns the full match.
With capture groups, `.group(1)`, `.group(2)`, etc. return individual groups.

### `.start()` vs `.span()`

`.start()` returns the start index of the match as a plain integer:

```python
m.start()   # e.g. 1
```

`.span()` returns a tuple of `(start, end)`:

```python
m.span()    # e.g. (1, 2)
```

Use `.start()` when you only need the position -- no unpacking needed. Use `.span()`
when you need both boundaries, for example to slice the matched substring back out of
the original text.

```python
# extracting just position -- cleaner with .start()
[(m.group(), m.start()) for m in pattern.finditer(text)]

# vs the longer form using .span()
[(m.group(), m.span()[0]) for m in pattern.finditer(text)]
```
