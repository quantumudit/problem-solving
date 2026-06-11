---
platform: stratascratch
problem_id: "10352"
slug: users_by_avg_session_time
difficulty: medium
difficulty_rating: medium
language: [sql, pandas, polars]
topics: [aggregation, datetime, filtering, cte, joins, date_functions, case_when]
date_solved: 2026-06-11
revisit: false
---

## Approach

For each user and date, find the latest `page_load` timestamp and the earliest
`page_exit` timestamp. A valid session requires the load to come before the exit on the
same day. Compute the duration per session, discard invalid ones, then average per user.

All three solutions follow the same logic -- they differ only in how they express the
per-day grouping and the validity filter.

## SQL Variants

Three progressively cleaner SQL solutions:

- `solution.sql` (CTE) -- two CTEs compute `load_time` and `exit_time` separately, then
  join them with `load_time < exit_time` as a join condition.
- `solution_v2.sql` (subquery + `CASE WHEN`) -- one subquery collapses load and exit into
  the same row using `MAX(CASE WHEN action = 'page_load' THEN timestamp END)`.
- `solution_v3.sql` (subquery + `FILTER`) -- same as v2 but uses the cleaner
  `MAX(timestamp) FILTER (WHERE action = 'page_load')` syntax.

## Tricks / New Learnings

**Pandas -- MultiIndex Series subtraction as a free inner join**

Keeping `loads` and `exits` as Series with a `["user_id", "date"]` MultiIndex (by not
calling `.reset_index()`) lets you subtract them directly:

```python
durations = exits - loads
```

Pandas aligns on matching index keys before subtracting, which acts as an inner join on
`(user_id, date)` -- no explicit `pd.merge()` needed.

**Pandas -- validating session order with `pd.Timedelta(0)`**

Rather than comparing the original timestamp columns from `loads` and `exits`, filtering
on the computed duration is cleaner and more direct:

```python
valid_durations = durations[durations > pd.Timedelta(0)]
```

**SQL -- `FILTER` keyword (v3)**

`MAX(timestamp) FILTER (WHERE action = 'page_load')` replaces the verbose `CASE WHEN`
pattern. Supported in: PostgreSQL, DuckDB, SparkSQL 3.0+. Use `CASE WHEN` for MSSQL.

**SQL -- casting a timestamp to date**

| Syntax | Dialect |
|---|---|
| `timestamp::DATE` | PostgreSQL, DuckDB |
| `CAST(timestamp AS DATE)` | All dialects |
| `TO_DATE(timestamp)` | SparkSQL |

For duration calculation in non-PostgreSQL dialects:
- SparkSQL: `AVG(UNIX_TIMESTAMP(exit_time) - UNIX_TIMESTAMP(load_time))`
- MSSQL: `AVG(CAST(DATEDIFF(second, load_time, exit_time) AS FLOAT))`

**Polars -- `filter()` inside `agg()` for single-pass per-group computation**

Instead of filtering the whole DataFrame twice, Polars applies the filter inside the
aggregation expression itself:

```python
pl.col("timestamp").filter(pl.col("action") == "page_load").max()
```

This computes the max load time and min exit time in a single pass over each group,
without creating intermediate DataFrames.

## Performance: Polars vs Pandas

| Factor | Pandas | Polars |
|---|---|---|
| Memory | Creates separate `loads` and `exits` objects in memory | Computes final duration directly -- no intermediate tables |
| Evaluation | Applies filters and subtraction in separate steps | Single-pass via Expression API -- filters and math run together |
| Parallelism | Mostly single-threaded for `groupby` operations | Built on Rust -- parallelizes aggregations across all CPU cores |
