---
platform: alteryx_community
problem_id: "0013"
slug: running_averages
difficulty: medium
link: https://community.alteryx.com/t5/Weekly-Challenge/Challenge-3-Running-Averages/td-p/36814
dataset: provided
---

# Running Averages

## Problem
[Alteryx Community - Challenge 3: Running Averages](https://community.alteryx.com/t5/Weekly-Challenge/Challenge-3-Running-Averages/td-p/36814)

## Problem Statement
Create 3-month and 6-month running averages by RM Category for the following columns:

- `c.LK98`
- `p.LK98`
- `c.1K`
- `p.1K`
- `c.NLP3`
- `p.NLP3`

## Dataset

| File | Description |
|---|---|
| `data/rm_categories.csv` | Monthly values per RM Category |

## Steps

1. Group data by RM Category
2. For each of the six value columns, compute a 3-month rolling average
3. For each of the six value columns, compute a 6-month rolling average
4. Output the results alongside the original data

## Concepts Covered
- Data preparation
- Rolling / sliding window aggregations
- Grouped time-series calculations
