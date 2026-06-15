---
platform: misc
problem_id: "0005"
slug: madlibs
difficulty: null
difficulty_rating: medium
language: [python]
topics: [string_ops, conditional_logic]
date_solved: 2026-06-14
revisit: false
---

# Notes

## `str.format()` -- Named Placeholder Substitution

`str.format()` replaces `{placeholder}` tokens in a string with provided values.
Placeholders can be positional (by index) or named (by keyword):

```python
# positional -- replaced by argument order
"{} went to {}".format("Alice", "Paris")
# "Alice went to Paris"

# named -- replaced by keyword argument name
"{name} went to {place}".format(name="Alice", place="Paris")
# "Alice went to Paris"
```

Named placeholders are cleaner when the template has many substitutions or when
the same placeholder appears more than once -- you name it once, it fills everywhere:

```python
"{name} said hello. Everyone waved back at {name}.".format(name="Alice")
# "Alice said hello. Everyone waved back at Alice."
```

---

## Passing a Dict to `format()` -- The `**` Unpack

`str.format()` takes keyword arguments, not a dict directly. To use a dict, you
unpack it with `**`:

```python
words = {"name": "Alice", "place": "Paris"}

"{name} went to {place}".format(**words)
# "Alice went to Paris"
```

The `**` unpacks the dict into keyword arguments at the call site. This works but
requires the entire dict to be unpacked upfront.

---

## `str.format_map()` -- Pass the Dict Directly

`format_map()` does the same substitution but accepts a dict (or any mapping)
directly -- no `**` unpacking needed:

```python
words = {"name": "Alice", "place": "Paris"}

"{name} went to {place}".format_map(words)
# "Alice went to Paris"
```

For basic use with a plain dict, `format(**words)` and `format_map(words)` produce
identical results. The idiomatic choice when you already have a dict is `format_map`.

---

## Key Difference -- How Missing Keys Are Handled

`format(**dict)` unpacks everything upfront, so a missing key raises `KeyError`
before substitution even begins.

`format_map(dict)` looks up each key lazily as it substitutes. This means you can
pass a custom dict-like object with a `__missing__` method to control what happens
when a key is absent:

```python
from collections import defaultdict

words = defaultdict(lambda: "???")
words["name"] = "Alice"

"{name} went to {place}".format_map(words)
# "Alice went to ???"    <- missing key handled gracefully

"{name} went to {place}".format(**words)
# KeyError: 'place'      <- blows up before substitution
```

---

## How format_map() Was Used in This Problem

`fill_madlib` is a one-liner built on `format_map`:

```python
def fill_madlib(template: str, words: dict[str, str]) -> str:
    return template.format_map(words)
```

Because `format_map` treats values as plain strings, the solution uses a neat trick
to highlight filled words in the output -- it wraps each value in Rich markup before
substitution:

```python
highlighted = {k: f"[bold cyan]{v}[/bold cyan]" for k, v in words.items()}
fill_madlib(template, highlighted)
```

`format_map` just substitutes the markup strings in as-is. Rich renders them when
the result is printed, so the user-supplied words appear highlighted in the final
story without any extra parsing step.
