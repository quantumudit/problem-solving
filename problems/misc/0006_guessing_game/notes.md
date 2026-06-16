---
platform: misc
problem_id: "0006"
slug: guessing_game
difficulty: null
difficulty_rating: easy
language: [python]
topics: [conditional_logic, stateful_iteration]
date_solved: 2026-06-14
revisit: false
---

# Notes

## Dict as a Lookup Table Instead of if/else Chains

When multiple branches only differ by which value they return, a dict is cleaner
than an if/else chain. The key selects the value directly, with no branching logic.

```python
# if/else -- grows with every new difficulty level
if difficulty == "easy":
    low, high = 1, 50
elif difficulty == "medium":
    low, high = 1, 100
elif difficulty == "hard":
    low, high = 1, 500

# dict lookup -- adding a new difficulty is one line in the dict
DIFFICULTY_RANGES = {
    "easy":   (1, 50),
    "medium": (1, 100),
    "hard":   (1, 500),
}

low, high = DIFFICULTY_RANGES[difficulty]
```

The same pattern works for any per-key config: attempt limits, colors, labels.
In this problem, both `DIFFICULTY_RANGES` and `MAX_ATTEMPTS` use it:

```python
MAX_ATTEMPTS: dict[str, int | None] = {
    "easy":   None,   # unlimited
    "medium": 10,
    "hard":   7,
}
```

The `None` value for easy is idiomatic Python for "not applicable" -- no special
sentinel needed. The caller checks `if max_att is not None` to decide whether
to enforce a limit.
