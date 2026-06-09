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

Comments are welcome when they add explanation value or enhance readability.

Good reasons to add a comment:
- A non-intuitive invariant or edge case being handled
- A math trick or algorithmic choice that is not immediately clear
- Section headers that help orient a reader in longer scripts
- A brief note clarifying a non-obvious step in a data pipeline

Avoid comments that merely restate what the code already says clearly through good naming.

---

## Imports

Import only what the solution needs. Standard library and common data science packages are fine:

```python
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop
import pandas as pd
```

No project-local imports except `from utils import ...` -- the `utils/` package is the one shared library allowed in this repo.

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

## Interview Prep Context

These solutions serve a dual purpose: correctness practice and interview preparation.
As a result, the following are acceptable and encouraged:

- `print()` statements that trace intermediate steps (e.g. month-by-month acquisition log)
- Verbose variable names that communicate reasoning clearly to an interviewer
- Step-by-step logic over one-liners when clarity matters more than brevity

---

## What does NOT apply here

- Module docstrings -- solution files don't need them
- `CustomException`, shared loggers, config loaders -- no shared infrastructure in this repo
- `from __future__ import annotations` -- not needed for standalone solution files

For running solutions that need external packages (pandas, numpy), see the
`use-virtual-environment` skill.
