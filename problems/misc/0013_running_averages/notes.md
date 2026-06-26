---
platform: alteryx_community
problem_id: "0013"
slug: running_averages
difficulty: medium
difficulty_rating: medium
language: [pandas]
topics: [reshaping, aggregation]
date_solved: 2026-06-26
revisit: true
---

# Notes

Revisit to add Polars solution.

## Wide-to-Long Reshape with `pd.melt()`

The raw data has one column per metric (wide format). Melting it into long format
lets a single `groupby().rolling()` call handle all metrics at once.

```python
long_df = pd.melt(
    raw_df,
    id_vars=id_cols,        # columns to keep as-is (RM Category, Year, Month)
    value_vars=metric_cols, # columns to collapse into rows
    var_name="Metric",      # new column holding the old column names
    value_name="Value",     # new column holding the values
)
```

Without melting, you would need a separate rolling calculation per metric column.

---

## Auto-detecting Column Types with `select_dtypes()`

Instead of hardcoding column names, `select_dtypes()` separates ID columns from
metric columns based on dtype alone.

```python
id_cols = raw_df.select_dtypes(exclude=["float64"]).columns   # Year, Month, RM Category
metric_cols = raw_df.select_dtypes(include=["float64"]).columns  # c.LK98, p.LK98, ...
```

This is robust to schema changes -- adding a new float column automatically includes
it in the rolling calculation without touching the code.

---

## Grouped Rolling Windows

`rolling()` computes a sliding window aggregation. When chained after `groupby()`,
the window is applied independently within each group.

```python
prepared_df.groupby(["Metric", "RM Category", "Year"])["Value"]
    .rolling(window=3, min_periods=1)
    .mean()
```

Key arguments:
- `window=3` -- size of the sliding window (3 periods)
- `min_periods=1` -- compute a partial average at the start instead of returning NaN
  for the first `window - 1` rows

---

## Index Realignment After Grouped Rolling

`rolling()` on a `groupby` re-attaches the group keys as extra index levels on the
result. This misaligns the Series with the original DataFrame index, breaking
`pd.concat(axis=1)`.

```python
.reset_index(level=[0, 1, 2], drop=True)  # drop the 3 groupby key levels
```

`level=[0, 1, 2]` matches the three groupby keys (Metric, RM Category, Year).
`drop=True` discards them instead of promoting them to columns. After this, the
Series index matches `prepared_df` and the concat aligns correctly by position.
