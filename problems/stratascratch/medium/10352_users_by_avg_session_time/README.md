---
platform: stratascratch
problem_id: "10352"
slug: users_by_avg_session_time
difficulty: medium
link: https://platform.stratascratch.com/coding/10352-users-by-avg-session-time
dataset: platform
---

## Problem
[StrataScratch 10352 - Users By Average Session Time](https://platform.stratascratch.com/coding/10352-users-by-avg-session-time)

## Problem Statement

Calculate each user's average session time, where a session is defined as the time
difference between a `page_load` and a `page_exit`. Assume each user has only one session
per day. If there are multiple `page_load` or `page_exit` events on the same day, use only
the latest `page_load` and the earliest `page_exit`. Only consider sessions where the
`page_load` occurs before the `page_exit` on the same day. Output the `user_id` and their
average session time.

## Input Schema

**facebook_web_log**

| Column | Type |
|---|---|
| user_id | bigint |
| timestamp | timestamp without time zone |
| action | text |

## Output

| Column | Description |
|---|---|
| user_id | User identifier |
| avg_session_time | Average session duration across all qualifying days |

## Files

- [solution.sql](solution.sql)
- [solution_v2.sql](solution_v2.sql)
- [solution_v3.sql](solution_v3.sql)
- [solution_pandas.py](solution_pandas.py)
- [solution_polars.py](solution_polars.py)
- [notes.md](notes.md)
