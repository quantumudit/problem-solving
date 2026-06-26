---
platform: alteryx_community
problem_id: "0016"
slug: womens_world_cup_wins
difficulty: easy
difficulty_rating: easy
language: [pandas]
topics: [conditional_logic, aggregation, sorting]
date_solved: 2026-06-26
revisit: true
---

# Notes

Revisit to add Polars solution.

## Vectorized Conditional Column Creation with `np.select()`

`np.select(conditions, choices, default)` creates a new column based on a list of
conditions evaluated in order. The first condition that is True for a row determines
the value for that row. If no condition matches, `default` is used.

```python
conditions = [
    raw_df["score_i"] > raw_df["score_j"],  # Team_i won
    raw_df["score_i"] < raw_df["score_j"],  # Team_j won
]
choices = [raw_df["Team_i"], raw_df["Team_j"]]

raw_df["winner"] = np.select(conditions, choices, default="")
# draws (equal scores) fall through to default -- empty string
```

This is the vectorized equivalent of a chained `if/elif/else` applied row-by-row.
It is far faster than `apply()` for large DataFrames.

---

## Removing Empty Strings via Regex Replace + `dropna()`

`np.select` sets the default to `""` for draws. `value_counts()` includes these
empty-string rows in the result. To drop them cleanly:

```python
.replace(r"^\s*$", np.nan, regex=True)  # empty or whitespace-only -> NaN
.dropna(subset=["winner"])              # drop NaN rows in the winner column
```

The regex `^\s*$` matches strings containing nothing or only whitespace. Replacing
with NaN first allows `dropna()` to handle the removal, which is more explicit than
a boolean filter and also catches whitespace-only entries.

---

## Ranking a Column with `rank()`

Unlike the grouped case (0015), this problem ranks all teams globally --
so `rank()` is called directly on the column, not via `groupby()`.

```python
wins_df["winner_rank"] = wins_df["count"].rank(ascending=False, method="dense").astype("int64")
```

`ascending=False` makes rank 1 the highest win count. `method="dense"` avoids gaps
if any two teams share the same number of wins.
