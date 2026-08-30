---
platform: projects
slug: olympic_history_analysis
difficulty: null
difficulty_rating: null
language: [sql]
topics: [aggregation, joins, window_functions, cte, subqueries, having, case_when, string_manipulation, filtering, sorting]
date_solved: null
revisit: false
---

## Approach

## Key Observations

## Tricks / New Learnings

### q04 -- subquery vs window function for min/max filtering

Two ways to find the Games with the highest and lowest nation count:

**v1 -- correlated subqueries in WHERE**

```sql
WHERE nations_participated = (SELECT MAX(nations_participated) FROM cte)
```

Readable, but scans the CTE 3 times: once for the main SELECT, once for MAX, once for MIN.

**v2 -- window functions (preferred)**

```sql
RANK() OVER (ORDER BY nations_participated ASC)   -- Lowest
RANK() OVER (ORDER BY nations_participated DESC)  -- Highest
```

Computes both rankings in a single pass over the data. Two total scans vs three.
Scales better and avoids repeated aggregation sub-scans.

Rule: when you need to filter rows by a min/max of the same dataset, prefer
`RANK() OVER (ORDER BY ...)` + `WHERE rnk = 1` over correlated subqueries.

### q10 -- TRY_CAST vs CAST vs :: for "NA"-polluted numeric columns

The `Age`, `Height`, and `Weight` columns are stored as VARCHAR in the CSV because
missing values are the string `"NA"`, not SQL NULLs (see data README).

When you need to sort or do arithmetic on these columns, you must cast them:

| Syntax | Behavior on "NA" | Safe to use? |
|---|---|---|
| `CAST(Age AS INTEGER)` | Throws a runtime error | No |
| `Age::INTEGER` | Same as CAST -- throws an error | No |
| `TRY_CAST(Age AS INTEGER)` | Returns NULL instead of erroring | Yes |

`CAST` and `::` are identical -- `::` is just shorthand. Both fail hard on any
non-numeric string, so "NA" breaks them.

`TRY_CAST` is the safe choice: it converts what it can and silently returns NULL
for anything it cannot parse.

**Why the bug in q10 is hidden:** even without TRY_CAST, the `WHERE Age != 'NA'`
filter removes the bad rows before the cast in most execution plans. But this
depends on evaluation order, which the engine does not guarantee. TRY_CAST makes
the intent explicit and protects against edge cases.

**When lexicographic sort coincidentally works:** ordering VARCHAR ages like "60",
"63", "64" gives the correct result because all values have the same number of
digits. The bug surfaces when mixed-length values appear, e.g. "9" sorts after
"64" lexicographically but is numerically smaller.

Rule: always use `TRY_CAST` when a column is VARCHAR but represents a number, and
filter `WHERE col != 'NA'` before any arithmetic.

### q13 -- pivoting long format to wide format with CASE WHEN

When a column holds a category (e.g. `Medal = 'Gold' / 'Silver' / 'Bronze'`) and
you want each category as its own column, use `COUNT(CASE WHEN ... THEN 1 END)`:

```sql
-- Long format (one row per country per medal type)
SELECT region, Medal, COUNT(*) AS total
FROM ...
GROUP BY region, Medal

-- Wide format (one row per country, one column per medal type)
SELECT
    region,
    COUNT(CASE WHEN Medal = 'Gold'   THEN 1 END) AS gold,
    COUNT(CASE WHEN Medal = 'Silver' THEN 1 END) AS silver,
    COUNT(CASE WHEN Medal = 'Bronze' THEN 1 END) AS bronze
FROM ...
GROUP BY region
```

**How it works:** `CASE WHEN` returns `1` for matching rows and `NULL` for
everything else. `COUNT` ignores NULLs, so each column only counts its own
category. No `WHERE Medal != 'NA'` needed -- non-matching values (including
`'NA'`) return NULL and are silently skipped.

**Alignment trick:** pad the category strings so the `THEN` keywords line up --
makes the pattern easier to scan at a glance.

**When to use long vs wide:**
- Long: easier to aggregate further, filter, or join on the category
- Wide: easier to read as a report, required when comparing columns side by side

## Revisit notes
