---
platform: stratascratch
problem_id: "10353"
slug: workers_with_the_highest_salaries
difficulty: easy
link: https://platform.stratascratch.com/coding/10353-workers-with-the-highest-salaries
dataset: platform
---

## Problem
[StrataScratch 10353 - Workers With The Highest Salaries](https://platform.stratascratch.com/coding/10353-workers-with-the-highest-salaries)

## Problem Statement

Management wants to analyze only employees with official job titles. Find the job titles
of the employees with the highest salary. If multiple employees have the same highest
salary, include all their job titles.

## Input Schema

**worker**

| Column | Type |
|---|---|
| worker_id | bigint |
| first_name | text |
| last_name | text |
| salary | bigint |
| joining_date | date |
| department | text |

**title**

| Column | Type |
|---|---|
| worker_ref_id | bigint |
| worker_title | text |
| affected_from | date |

## Output

| Column | Description |
|---|---|
| worker_title | Job title of the employee(s) with the highest salary |

## Files

- [solution.sql](solution.sql)
- [solution_pandas.py](solution_pandas.py)
- [solution_polars.py](solution_polars.py)
- [notes.md](notes.md)
