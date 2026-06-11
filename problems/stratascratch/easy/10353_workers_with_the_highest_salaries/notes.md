---
platform: stratascratch
problem_id: "10353"
slug: workers_with_the_highest_salaries
difficulty: easy
difficulty_rating: easy
language: [sql, pandas, polars]
topics: [joins, filtering, window_functions]
date_solved: 2026-06-11
revisit: false
---

## Approach

Join `worker` and `title` on `worker_id = worker_ref_id` to pair each employee with their
job title, then keep only the rows where `salary` equals the global maximum. Deduplicate
in case the same title appears more than once.

All three solutions (SQL, pandas, polars) share the same shape:
join -> filter on max salary -> deduplicate.

## Tricks / New Learnings

**Pandas -- `.loc` with a lambda for in-chain filtering**

Using `lambda df:` inside `.loc` lets you reference the live DataFrame mid-chain without
saving an intermediate variable:

```python
.loc[lambda df: df["salary"] == df["salary"].max(), ["worker_title"]]
```

The lambda receives the DataFrame at that point in the chain, so `.max()` runs on the
already-joined result -- no temporary assignment needed.

**SQL -- prefer `RANK()` over `IN` or a correlated subquery**

Three approaches work:

- `WHERE salary IN (SELECT MAX(salary) FROM worker)` -- correct, but requires a second scan
- `JOIN` on a max-salary subquery -- similar cost, more verbose
- `RANK() OVER (ORDER BY salary DESC) = 1` -- single pass, tie-safe, cleaner intent

`RANK()` is the preferred choice: it handles ties by design, avoids a subquery, and the
optimizer can compute it in one pass over the joined result.
