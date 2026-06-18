---
platform: alteryx_community
problem_id: "0011"
slug: join_to_range
difficulty: medium
difficulty_rating: medium
language: [pandas, polars]
topics: [pandas_merge, pandas_groupby, string_ops]
date_solved: 2026-06-18
revisit: true
---

## Approach

### Pandas

Parse the range strings ("2000-2019") from the regions table into a list of (low, high) int
tuples before the join. Then use `.apply()` to tag each customer row with the matching range
label, and do a standard inner merge on that label to bring in Region, Sales Rep, etc.
Finish with a groupby count.

The key constraint pandas cannot escape: range-based joins are not natively supported, so the
match must happen row-by-row in Python via `.apply()` before the merge can run.

### Polars

Parse the range bounds as new columns directly on the regions frame using vectorized string
ops (`.str.split().list.first/last().cast(Int64)`). Then call `join_where()` with inequality
conditions -- this performs the non-equi join at the Rust level without touching Python objects.
Finish with `.group_by().agg(pl.len())`.

No `.apply()`, no intermediate label column, no Python loop -- the entire pipeline is
vectorized end to end.

## Pandas vs Polars

| Aspect | Pandas | Polars |
|---|---|---|
| Range matching | `.apply()` row-by-row (Python loop) | `join_where()` vectorized at Rust level |
| Intermediate step | Must create a label column, then merge | Direct non-equi join, no label needed |
| String parsing | Manual list comprehension outside the chain | `.str.split().list.first/last().cast()` inline |
| Count aggregation | `.count()` on a named column | `pl.len()` -- optimized row count, no column needed |
| Performance on large data | Slow due to Python overhead in `.apply()` | Significantly faster |

## What tripped me up

The Pandas merge call was initially written as:

```python
customers.merge(region, how="inner", left_on=customers["range"], right_on=region["Range"])
```

Passing Series objects instead of column name strings. This works but creates a `key_0` column
in the output instead of preserving the named columns. Should always use string names:

```python
customers.merge(region, how="inner", left_on="range_label", right_on="Range")
```

## Tricks / New Learnings

`join_where()` in Polars is the idiomatic way to do non-equi joins. It avoids the label-then-
merge pattern that Pandas forces you into and keeps the entire operation in the Rust execution
layer.

`pl.len()` vs `.count("column")` in Polars: `pl.len()` counts rows in the group directly --
it does not require a column reference and is slightly more expressive when the column being
counted is just a proxy for "how many rows are in this group."

## Revisit notes

Come back to write a SQL solution (DuckDB or SQLite). SQL handles range joins natively with
a `JOIN ... ON col BETWEEN low AND high`, which maps cleanly to this problem.
