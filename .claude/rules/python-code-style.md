---
paths:
  - "**/*.py"
---

# Python Code Style

Solution files in this repo are standalone -- no shared utilities, no project structure to follow.
Each `solution.py` solves one problem and is read in isolation.

---

## File Structure

A solution file contains the solution only -- no boilerplate, no test runner, no
`if __name__ == "__main__"` unless the problem explicitly requires it.

**LeetCode / StrataScatch style** (class-based):
```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in seen:
                return [seen[diff], i]
            seen[n] = i
        return []
```

**Pandas / SQL-equivalent style** (function-based):
```python
import pandas as pd

def top_earning_sales(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("employee_id")["salary"]
        .sum()
        .reset_index()
        .sort_values("salary", ascending=False)
        .head(5)
    )
```

---

## Type Hints

Use on all function signatures -- parameters and return types.

```python
def two_sum(self, nums: list[int], target: int) -> list[int]: ...
def length_of_longest_substring(self, s: str) -> int: ...
def merge(self, intervals: list[list[int]]) -> list[list[int]]: ...
```

- Use built-in generics: `list[int]`, `dict[str, int]`, `tuple[int, ...]`
- Use `X | None` instead of `Optional[X]`
- Use `X | Y` instead of `Union[X, Y]`
- Import `Any` from `typing` only if genuinely needed -- avoid it

---

## Naming

| Kind | Style | Example |
|---|---|---|
| Variables | `snake_case` | `left_ptr`, `max_sum`, `char_count` |
| Functions / methods | `snake_case` | `two_sum()`, `max_profit()` |
| Classes | `PascalCase` | `Solution`, `ListNode`, `TreeNode` |
| Constants | `UPPER_SNAKE_CASE` | `MOD = 10**9 + 7` |

- Names must be meaningful -- a reader should understand what a variable holds without a comment
- Avoid `res`, `ans`, `temp`, `val`, `data` -- name what the value actually represents
- Single-letter names are fine in tight loops (`for i, c in enumerate(s)`) or well-known
  math contexts (`l, r = 0, len(nums) - 1`)

---

## Comments

Write no comments by default. Code should be self-explanatory through good naming.

Add a comment only when the **why** is non-obvious:
- A non-intuitive invariant (`# right boundary is exclusive`)
- A specific edge case being handled (`# empty string returns 0, not -1`)
- A math trick that is not immediately clear

Never write comments that describe **what** the code does -- good names do that.

---

## Imports

Import only what the solution needs. Standard library and common data science packages are fine:

```python
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop
import pandas as pd
```

No project-local imports -- solution files are standalone.

---

## Style

- Line length: 88 characters max
- Use f-strings for string interpolation
- Use `is None` / `is not None` -- never `== None`
- Prefer readability over brevity: `left_pointer` over `lp`, but `l` is fine in a two-pointer loop
- Pandas chains: use parentheses for multi-line method chaining rather than backslashes

```python
# good
result = (
    df.groupby("category")["value"]
    .sum()
    .reset_index()
    .rename(columns={"value": "total"})
)

# avoid
result = df.groupby("category")["value"].sum().reset_index().rename(columns={"value": "total"})
```

---

## What does NOT apply here

- Module docstrings -- solution files don't need them
- `CustomException`, shared loggers, config loaders -- no shared infrastructure in this repo
- `from __future__ import annotations` -- not needed for standalone solution files

For running solutions that need external packages (pandas, numpy), see the
`use-virtual-environment` skill.
