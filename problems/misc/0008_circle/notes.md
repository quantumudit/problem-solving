---
platform: misc
problem_id: "0008"
slug: circle
difficulty: null
difficulty_rating: medium
language: [python]
topics: [conditional_logic]
date_solved: 2026-06-14
revisit: false
---

# Notes

## Dunder Methods -- Making Objects Behave Like Built-in Types

Dunder methods (double-underscore methods) let a class hook into Python's built-in
operations. Instead of calling methods explicitly, the object responds naturally to
operators and built-in functions.

| Dunder    | Triggered by          | Purpose in Circle                          |
|-----------|-----------------------|--------------------------------------------|
| `__repr__`| `print(c)`, `repr(c)` | Readable string: `Circle(radius=5.0)`      |
| `__eq__`  | `c1 == c2`            | Equal if same radius                       |
| `__lt__`  | `c1 < c2`, `sorted()` | Compare by area (smaller area = less-than) |
| `__add__` | `c1 + c2`             | New circle with combined radius            |

Implementing `__lt__` and `__eq__` together makes the class fully sortable:

```python
circles = [Circle(5), Circle(2), Circle(8)]

sorted(circles)          # [Circle(2.0), Circle(5.0), Circle(8.0)]
min(circles)             # Circle(radius=2.0)
max(circles)             # Circle(radius=8.0)
```

Python derives `>`, `>=`, `<=` from `__lt__` and `__eq__` automatically via
`functools.total_ordering` -- or they just work because Python inverts `__lt__`
for `>` comparisons.

---

## `isinstance()` + `NotImplemented` in Dunder Methods

When a dunder method receives an operand of the wrong type, the correct response
depends on the operation:

- For `__eq__`: return `False` -- "this circle is not equal to a non-circle"
- For `__lt__`, `__add__`: return `NotImplemented` -- tells Python to try the
  other operand's reflected method (`__gt__`, `__radd__`) before raising a TypeError

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Circle):
        return False           # definitive answer: not equal
    return self.radius == other.radius

def __lt__(self, other: object) -> bool:
    if not isinstance(other, Circle):
        return NotImplemented  # let Python try other.__gt__(self) first
    return self.area < other.area
```

Returning `NotImplemented` (not raising, not returning `False`) is the protocol
that allows Python's operator dispatch to work correctly with mixed types.

---

## `@property` -- Read-Only Computed Attributes

Storing derived values like `area` as plain instance attributes (`self.area = ...`)
makes them mutable -- anyone can do `circle.area = 999`. Using `@property` exposes
them as computed, read-only attributes with the same dot-access syntax:

```python
# instance attribute -- mutable, easy to corrupt
self.area = pi * self.radius ** 2

# property -- computed on access, read-only by default
@property
def area(self) -> float:
    return pi * self.radius ** 2
```

```python
c = Circle(5)
c.area          # 78.5398...  <- works
c.area = 999    # AttributeError: can't set attribute
```

The caller's code looks identical either way (`c.area`), but the property version
is always in sync with the current radius and cannot be silently overwritten.
