---
platform: excelbi
problem_id: "PQ00398"
slug: case_stage_progress
difficulty: null
link: https://lnkd.in/gg7thZjF
dataset: provided
---

## Problem
[ExcelBI - Case Stage Progress (PQ_Challenge_398)](https://lnkd.in/gg7thZjF)

## Problem Statement

A case processing pipeline moves each case through sequential numbered stages.
Each row in the dataset represents one stage for one case, with a flag indicating
whether that stage has been cleared.

For each CaseID, produce one summary row with the following columns:

| Output Column | Description |
|---|---|
| CurrentStage | Last stage where Cleared = TRUE (highest StageNo). "Not Started" if no stages are cleared. |
| NextStage | First stage where Cleared = FALSE after CurrentStage. "Completed" if all stages are cleared. |
| Status | "Not Started" / "In Progress" / "Completed" |
| ProcessIssue | "Yes" if a higher-numbered stage is cleared while a lower-numbered stage is not (out-of-order completion). "No" otherwise. |
| ProgressPct | Percentage of cleared stages out of total stages for that case (e.g. 3 of 5 = 60%). |

## Input Schema

| Column | Type | Description |
|---|---|---|
| CaseID | string | Case identifier |
| StageNo | integer | Numeric stage order (10, 20, 30, ...) |
| StageName | string | Human-readable stage label |
| Cleared | boolean | Whether the stage has been completed |

Pipeline stages (in order):
KYC Received (10) -> KYC Verified (20) -> Risk Review (30) -> Account Approval (40) -> Account Opened (50)

Note: not all cases have all 5 stages in the dataset.

## Example

**Input (selected rows):**

| CaseID | StageNo | StageName | Cleared |
|---|---|---|---|
| C1001 | 10 | KYC Received | TRUE |
| C1001 | 20 | KYC Verified | TRUE |
| C1001 | 30 | Risk Review | TRUE |
| C1001 | 40 | Account Approval | FALSE |
| C1001 | 50 | Account Opened | FALSE |
| C1005 | 10 | KYC Received | TRUE |
| C1005 | 20 | KYC Verified | TRUE |
| C1005 | 30 | Risk Review | FALSE |
| C1005 | 40 | Account Approval | TRUE |
| C1005 | 50 | Account Opened | FALSE |

**Expected output (for these two cases):**

| CaseID | CurrentStage | NextStage | Status | ProcessIssue | ProgressPct |
|---|---|---|---|---|---|
| C1001 | Risk Review | Account Approval | In Progress | No | 60% |
| C1005 | KYC Verified | Risk Review | In Progress | Yes | 60% |

C1005 has ProcessIssue = "Yes" because Account Approval (stage 40) is cleared while
Risk Review (stage 30) is not -- stages completed out of order.

## Files

- [solution.sql](solution.sql)
- [solution_pandas.py](solution_pandas.py)
- [solution_polars.py](solution_polars.py)
- [solution_duckdb.py](solution_duckdb.py)
- [solution_pyspark.py](solution_pyspark.py)
- [notes.md](notes.md)
- [data/cases.csv](data/cases.csv)

## Source

- [LinkedIn Post by ExcelBI](https://www.linkedin.com/posts/excelbi_challenge-powerquerychallenge-daxchallenge-activity-7469254725813616640-u6l5?utm_source=share&utm_medium=member_desktop&rcm=ACoAAByBXHwBWbdpEpS1fnfvxD21zkOGmmhNQWU) -- PQ_Challenge_398, posted 2026-06-07
