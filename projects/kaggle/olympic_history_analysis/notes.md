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

## Revisit notes
