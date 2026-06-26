---
platform: alteryx_community
problem_id: "0011"
slug: join_to_range
difficulty: medium
link: https://community.alteryx.com/t5/Weekly-Challenge/Challenge-1-Join-to-Range/td-p/36621
dataset: provided
---

# Join to Range

## Problem
[Alteryx Community - Challenge 1: Join to Range](https://community.alteryx.com/t5/Weekly-Challenge/Challenge-1-Join-to-Range/td-p/36621)

## Problem Statement
A company in Australia has source data made up of a series of postal codes (e.g. 2000, 2001,
2002) alongside other data fields. They have a separate reference table containing postcode
ranges (e.g. 2000 to 2002) which they want to use to match and filter their main data.

Each customer record must be joined to the lookup table based on a postal area ranged region.
Then summarize the customer data by Region, Sales Rep, and Responder, with a count of
customers.

## Datasets

| File                        | Description                                                      |
| --------------------------- | ---------------------------------------------------------------- |
| [data/customer_segment.csv](data/customer_segment.csv) | Main customer records with postal codes and other fields         |
| [data/region_range.csv](data/region_range.csv)     | Reference table with postcode range boundaries and region labels |

## Solutions

| File | Description |
|---|---|
| [solution.yxmd](solution.yxmd) | Alteryx workflow solution |
| [workflow.png](workflow.png) | Workflow diagram |
| [solution_pandas.py](solution_pandas.py) | Pandas solution |
| [solution_polars.py](solution_polars.py) | Polars solution |

## Steps

1. Join each customer record to the region lookup table where the customer postal code falls
   within the range defined in the lookup (range join, not exact match)
2. Summarize the joined data by Region, Sales Rep, and Responder
3. Output a count of customers per group

## Concepts Covered
- Data preparation
- Range-based joins (non-equi joins)
- Groupby aggregation
