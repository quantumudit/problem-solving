---
platform: projects
slug: demographic_data_analysis
difficulty: null
difficulty_rating: null
language: [pandas]
topics: [aggregation, filtering, sorting, joins, lambda_functions, conditional_logic]
date_solved: null
revisit: false
---

## Approach

The project is structured in three layers -- filtering (q01-q02), correlation and
visualization (q03-q05), and income-group-level deep dives (q06-q10). Each script
is self-contained: it loads the CSV, computes its slice of the analysis, and
displays the result via `show()`.

## Key Observations

- Birth rate is right-skewed: most countries cluster between 10-20, with a long
  tail of high-birth-rate countries mostly from Sub-Saharan Africa.
- There is a clear inverse relationship between birth rate and internet usage --
  countries with high birth rates tend to have very low internet penetration.
- Income group is a strong predictor of both metrics: high-income countries have
  low birth rates and high internet usage; low-income countries are the reverse.
- The Pearson correlation between birth rate and internet users is strongly
  negative at the overall level, and this pattern holds within each income group
  as well, though the strength varies.

## Tricks / New Learnings

**Named aggregations with `.agg()` (q06)**

The named aggregation syntax lets you apply multiple functions across multiple
columns in one call and immediately rename the output columns -- no chained
`.rename()` needed:

```python
df.groupby("Income Group").agg(
    country_count=("Country Name", "count"),
    avg_birth_rate=("Birth Rate", "mean"),
    avg_internet_users=("Internet Users", "mean"),
)
```

Each keyword argument is `output_col_name=(source_col, aggregation_func)`.

---

**Slicing `.describe()` output as a DataFrame (q07)**

`.describe()` returns a DataFrame with summary statistics as columns:
`count, mean, std, min, 25%, 50%, 75%, max`. After calling `.describe()`, you
can slice it like any DataFrame to keep only what you need:

```python
df.groupby("Income Group")["Birth Rate"].describe()[["min", "25%", "50%", "75%", "max"]]
```

The percentile column names include the `%` sign -- pass them as strings exactly
as they appear in the output.

---

**`idxmin()` / `idxmax()` on grouped data (q08)**

`idxmin()` and `idxmax()` return the *index label* of the min/max row, not the
value itself. On a grouped Series, they return one index per group. You then pass
those indices to `.loc[]` to retrieve the full rows from the original DataFrame:

```python
min_idx = df.groupby("Income Group")["Birth Rate"].idxmin()
df.loc[min_idx, ["Income Group", "Country Name", "Birth Rate"]]
```

`cols + ["Birth Rate"]` works because `cols` is a plain Python list -- list
concatenation creates a new list without mutating either original. Clean pattern
for reusing a base column list with one extra column added per use.

`df1.merge(df2)` vs `pd.merge(df1, df2)`: both produce the same result. The
method form (`df1.merge(df2)`) reads naturally when chaining and implies `df1`
is the left/primary frame. The function form (`pd.merge(df1, df2)`) is preferred
when both frames are equal inputs and neither is "primary". Use the method form
when inside a chain; use the function form when joining two independently built
DataFrames at the same level.

---

**`.apply()` with `pd.Series` for multi-column per-group output (q09)**

When you need multiple derived values per group as separate columns, returning
a `pd.Series` from the lambda is the right pattern. The Series keys become the
column names in the result:

```python
df.groupby("Income Group").apply(
    lambda g: pd.Series({
        "above_avg": (g["Birth Rate"] > global_avg).sum(),
        "below_avg": (g["Birth Rate"] <= global_avg).sum(),
    }),
    include_groups=False,
)
```

`include_groups=False`: from pandas 2.2+, groupby key columns present in the
DataFrame being passed to `apply` trigger a FutureWarning if included in the
group data. Setting `include_groups=False` explicitly excludes them from `g`
inside the lambda. The group key is still recovered via `.reset_index()`.

---

**Pearson correlation -- scalar and grouped (q10)**

`Series.corr(other)` computes the Pearson correlation between two Series and
returns a single float. For a quick overall result:

```python
df["Birth Rate"].corr(df["Internet Users"])
```

For grouped correlation, combine with `.apply()`:

```python
df.groupby("Income Group").apply(
    lambda g: g["Birth Rate"].corr(g["Internet Users"]),
    include_groups=False,
)
```

This runs the correlation independently within each group. The result is a
Series indexed by the group key; the correlation values come out in a column
named `0` by default, so rename it explicitly:

```python
.rename(columns={0: "pearson_correlation"})
```

## Revisit notes

