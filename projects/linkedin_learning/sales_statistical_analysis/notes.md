---
platform: projects
slug: sales_statistical_analysis
difficulty: null
difficulty_rating: null
language: [sql]
topics: [aggregation, window_functions, subqueries, date_functions, filtering, sorting]
date_solved: null
revisit: false
---

## Approach

SQL-only analysis using DuckDB as the in-process query engine. The raw data is a
pgSQL script (storedb.sql); build_dataset.py parses the INSERT statements and
produces a clean CSV. The runner loads that CSV as an in-memory view and executes
each question's .sql file.

Run a question:

```
just project-sql linkedin_learning sales_statistical_analysis q01
```

## Key Observations

_To be filled in after solving._

## Tricks / New Learnings

_To be filled in after solving._

## Revisit notes

_To be filled in after solving._
