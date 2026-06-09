---
platform: excelbi
problem_id: "PQ00398"
slug: case_stage_progress
difficulty: null
difficulty_rating: medium
language: [sql, pandas, polars, duckdb, pyspark]
topics: [aggregations, case_when, cte, window_functions, joins, pandas_groupby]
date_solved: 2026-06-09
revisit: false
---

## Approach

Group by CaseID and derive each output column independently:

- CurrentStage: highest-numbered cleared StageNo -> look up StageName. "Not Started" if none cleared.
- NextStage: first uncleared stage with StageNo > CurrentStageNo. "Completed" if none exist.
- Status: derived from ProgressPct -- 0% = "Not Started", 100% = "Completed", else "In Progress".
- ProcessIssue: "Yes" if max(cleared StageNo) > min(uncleared StageNo) -- out-of-order completion.
- ProgressPct: mean(Cleared) * 100 formatted as a percentage string.

SQL / PySpark: A `stage_summary` CTE / DataFrame pre-computes CurrentStageNo and
FirstUnclearedStageNo, then joins back to the raw table to resolve stage names.
ROW_NUMBER picks the first uncleared candidate after the current stage.

Pandas: `groupby().apply()` with one helper function per output column. Each helper
receives the group DataFrame and returns a scalar.

Polars: Declarative `group_by().agg()` using chained list expressions. `filter()`
inside `agg()` filters column values within the group before the aggregation runs.

## Complexity

- Time: O(n log n) -- sort within groups to pick first/last stage
- Space: O(n) -- one output row per CaseID

## What tripped me up

NextStage is the first uncleared stage *after CurrentStageNo*, not just the first
uncleared stage overall. For a case where stage 40 is cleared but stage 30 is not,
NextStage is stage 30 (the gap), not stage 50 (the next in sequence).

The "no stages cleared" edge case requires CurrentStageNo = 0 so that all uncleared
stages qualify as next-stage candidates and the smallest is picked correctly.

## Tricks / New Learnings

Polars `filter()` inside `agg()`: filters the values of a column within the current
group before the aggregation, without a separate `filter()` call on the DataFrame.

```python
pl.col("StageName")
    .sort_by("StageNo")
    .filter(pl.col("Cleared"))
    .last()
    .fill_null("Not Started")
```

Reads: "within each group, sort StageName by StageNo, keep only cleared rows,
take the last one, default to 'Not Started' if the filtered result is empty."

SQL COALESCE on the uncleared-stage min: wrapping the min with a sentinel value
(MAX(StageNo) + 1) means a fully-cleared case has FirstUnclearedStageNo > all
real stage numbers, so the ProcessIssue CASE cleanly returns 'No'.
