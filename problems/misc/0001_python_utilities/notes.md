---
platform: misc
problem_id: "0001"
slug: python_utilities
difficulty: null
difficulty_rating: easy
language: [python]
topics: [conditional_logic, stateful_iteration]
date_solved: 2026-06-13
revisit: false
---

# Notes

## Ternary Operator for Chained Conditions

`sign_and_parity` originally used an if/elif/else block to assign the sign label.
A chained ternary collapses it into a single expression without losing readability.

```python
# if/elif/else -- three branches, three assignments
if num > 0:
    sign = "Positive"
elif num < 0:
    sign = "Negative"
else:
    sign = "Zero"

# chained ternary -- one expression, same logic
sign = "Positive" if num > 0 else "Negative" if num < 0 else "Zero"
```

Works well when every branch is a simple value assignment and the conditions are
mutually exclusive and exhaustive. Avoid it when branches contain logic or side
effects -- it becomes hard to read fast.

---

## Union Types with `|` (Python 3.10+)

Before Python 3.10, union types required imports from `typing`.

```python
# pre-3.10 -- verbose, extra import
from typing import Optional, Union

def func(x: Optional[int]) -> Union[int, float]: ...
```

Python 3.10 introduced `|` directly in type hints, no import needed.

```python
# 3.10+ -- clean, no import
def func(x: int | None) -> int | float: ...
```

`Optional[X]` is exactly `X | None` -- the `|` form makes that explicit.
`Union[X, Y]` is exactly `X | Y`.

---

## `isinstance()` with `|` (Python 3.10+)

The `|` syntax also works inside `isinstance()`, replacing the old tuple form.

```python
# old -- tuple of types
isinstance(x, (int, float))

# new -- union with |
isinstance(x, int | float)
```

Both are equivalent at runtime. The `|` form is consistent with the type hint syntax
and reads more naturally.

```python
def sum_two_numbers(num1: int | float, num2: int | float) -> int | float:
    if not isinstance(num1, int | float) or not isinstance(num2, int | float):
        raise ValueError("Both inputs must be integers or floats")
    return num1 + num2
```

---

## Typer Does Not Support `|` in Parameter Types

Typer (built on Click) resolves CLI argument types at parse time. It does not
understand union types and raises an error if you annotate a parameter with `X | Y`.

```python
# this breaks -- Typer cannot derive a Click type from int | float
def add(num1: int | float = typer.Option(...)):
    ...
```

The fix is to use the wider type. `float` accepts both integer input ("3") and
float input ("2.5") from the command line, so it covers both cases without a union.

```python
# this works -- float handles "3" and "2.5" cleanly
def add(num1: float = typer.Option(...)):
    ...
```

Use `int | float` freely in `utils.py` (pure Python functions), but always
resolve to a single concrete type in the Typer layer.

---

## `typer.Option` vs `typer.Argument`

| Feature             | `typer.Argument`                                | `typer.Option`                                 |
| ------------------- | ----------------------------------------------- | ---------------------------------------------- |
| How value is passed | Positional -- by order on the command line      | Named -- always follows a flag (`--num`, `-n`) |
| Negative numbers    | Breaks -- `-4` is parsed as an unknown flag     | Works -- `-n -4` is unambiguous                |
| `prompt=` support   | No                                              | Yes -- falls back to interactive prompt        |
| Syntax on CLI       | `parity 7`                                      | `parity --num 7` or `parity -n 7`              |
| Best for            | Non-interactive scripts, always-positive values | Interactive tools, values that can be negative |

Click (and every standard CLI parser) reserves any token starting with `-` as a
potential flag. With `typer.Argument`, a value like `-4` is intercepted as an
unknown flag before our code ever sees it. With `typer.Option`, Click knows the
token after `--num` or `-n` is a value, not a flag.

```
python solution.py parity -n -4      # works -- "-4" is the value of -n
python solution.py parity            # falls back to prompt
# Enter an integer: -4               <- typed freely, no parsing conflict
```

Rule of thumb for this repo: use `typer.Option` for all interactive utility
commands. Reserve `typer.Argument` for non-interactive scripts where values are
always supplied and never negative.
