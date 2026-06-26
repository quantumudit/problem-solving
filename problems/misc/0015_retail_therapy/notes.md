---
platform: alteryx_community
problem_id: "0015"
slug: retail_therapy
difficulty: easy
difficulty_rating: easy
language: [pandas]
topics: [filtering, aggregation, sorting]
date_solved: 2026-06-26
revisit: true
---

# Notes

Revisit to add Polars solution.

## Grouped Ranking with `rank()` and `method="dense"`

`rank()` assigns a numeric rank to each value. When called on a grouped Series, it
ranks within each group independently -- the correct behavior for top-N-per-group problems.

```python
avg_ratings_df["Rating Rank"] = (
    avg_ratings_df.groupby("Class Name")["Rating"]
    .rank(ascending=False, method="dense")
    .astype(int)
)
```

The `method` argument controls how ties are handled:

| method | Behavior | Example (scores: 5, 4, 4, 3) |
|---|---|---|
| `dense` | Tied values share a rank; next rank increments by 1 | 1, 2, 2, 3 |
| `min` | Tied values get the lowest rank in the group | 1, 2, 2, 4 |
| `average` | Tied values get the average of their ranks | 1, 2.5, 2.5, 4 |
| `max` | Tied values get the highest rank in the group | 1, 3, 3, 4 |

`method="dense"` is the right choice here because it avoids gaps -- a score of 3 in
a tie-heavy class would still appear in the top 5 rather than being pushed out by a
large rank number.

`.astype(int)` converts float ranks (the default dtype) to integers for cleaner display.
