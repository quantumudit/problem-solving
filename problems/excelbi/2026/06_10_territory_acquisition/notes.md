---
platform: excelbi
problem_id: "PQ00397"
slug: territory_acquisition
difficulty: null
difficulty_rating: medium
language: [pandas, polars]
topics: [simulation, aggregation, stateful_iteration, string_ops]
date_solved: 2026-06-10
revisit: true
---

## Approach

* Convert month names into a sortable month number and process data chronologically.
* Maintain an ownership mapping (`territory -> owner`) that evolves after each month's acquisition.
* For each month:
  * Resolve the current owner of every territory.
  * Aggregate revenue at the owner level by summing revenues across all territories owned by the same owner.
  * Identify the highest-revenue owner and the lowest-revenue owner.
  * Transfer ownership of all territories belonging to the lowest-revenue owner to the highest-revenue owner.
* Stop early if only one owner remains.
* Generate the final ownership structure by grouping territories under their final owner.

---

## What tripped me up

* The problem statement was initially ambiguous.
* Verifying the expected output and walking through the simulation month-by-month revealed that owner revenues must be aggregated after acquisitions.
* A subtle implementation bug was updating ownership for only the losing territory.

---

## Tricks / New Learnings

* Stateful simulations are often easier to model with a small amount of mutable state and iteration than with complex declarative transformations.
* Polars can efficiently handle the aggregation and join logic, but the month-by-month ownership evolution still requires iteration because each month's state depends on the previous month's result.
* For simulation-style problems, a dictionary-based ownership map is often the simplest representation of evolving state.
* When building final grouped outputs, prefer grouping and aggregation over manually constructing result rows, as it generalizes correctly when multiple owners remain.
* Avoid updating only the losing owner's original territory: `owner_map[bottom] = top` This works for the sample data but fails when an owner controls multiple territories. Instead, transfer all territories owned by the losing owner:

```python
  for territory, owner in owner_map.items():
      if owner == bottom:
          owner_map[territory] = top
```
This correctly handles ownership consolidation and scales to larger datasets. In Polars, the solution is much more vectorized.

---

## Revisit notes

### Key Insight

This is not primarily a grouping or window-function problem. It is a **stateful simulation problem**.

The ownership structure changes after every month, and the ownership state from one month directly affects revenue calculations in future months.

The core pattern is:

```text
Current State
      ↓
Calculate Monthly Outcome
      ↓
Update State
      ↓
Next Month
```

Recognizing the state transition aspect is the most important part of the problem.

---

### Technology Comparison

| Approach                                   | Difficulty | Notes                                                                                                                                                          |
| ------------------------------------------ | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pandas                                     | ⭐         | Most natural solution. Mutable state and iterative logic map directly to the business rules.                                                                   |
| Polars                                     | ⭐         | Similar to Pandas. Uses Polars for aggregations while keeping ownership evolution in Python.                                                                   |
| PySpark                                    | ⭐⭐       | Requires a driver-side loop but uses Spark DataFrames for joins and aggregations. Ownership state can be stored in a DataFrame instead of a Python dictionary. |
| Python + DuckDB                            | ⭐⭐       | Similar to PySpark conceptually. Python controls the simulation while DuckDB performs aggregations and joins efficiently using SQL.                            |
| Recursive CTE (DuckDB/Postgres/SQL Server) | ⭐⭐⭐⭐   | Possible but significantly more complex. Ownership evolution must be encoded recursively, making the query harder to understand and maintain.                  |

---

### Why PySpark Is Easier Than Recursive SQL

PySpark still allows a straightforward month-by-month simulation:

```text
for month:
    aggregate revenue
    determine winner
    determine loser
    update ownership
```

The business logic remains explicit and easy to reason about.

Spark handles the expensive distributed operations (joins and aggregations), while Python controls the state transitions.

In contrast, recursive SQL must encode both the state and the transition logic inside a recursive query, making the implementation considerably harder to read and debug.

---

### Why Python + DuckDB Is Easier Than Recursive SQL

DuckDB allows ownership state to be managed externally while SQL handles aggregation work.

The workflow becomes:

```text
Python Loop
    ↓
Run DuckDB Aggregation
    ↓
Update Ownership
    ↓
Next Month
```

This keeps the simulation logic simple and separates state management from analytical queries.

Recursive SQL attempts to express the entire simulation inside a single query, which is technically possible but much less maintainable.

---

### Interview Takeaway

If asked whether SQL can solve this problem:

> Yes, using recursive CTEs or procedural SQL. However, SQL is not the most natural abstraction because ownership evolves over time. The problem is fundamentally a stateful simulation, making Python-based approaches (Pandas, Polars, PySpark, or Python + DuckDB) more intuitive and maintainable.

