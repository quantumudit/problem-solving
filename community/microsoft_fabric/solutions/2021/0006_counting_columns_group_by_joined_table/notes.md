---
community: microsoft_fabric
sno: "0006"
category: dax_commands_and_tips
slug: counting_columns_group_by_joined_table
topic_url: https://community.fabric.microsoft.com/t5/DAX-Commands-and-Tips/Counting-columns-and-group-by-another-column-in-a-joined-table/m-p/1755592#M36652
date_answered: 2021-03-31
accepted: false
language: [dax, pq]
topics: [summarize, groupby, aggregations, merge_queries]
---

## Problem

The user had two spreadsheets imported into Power BI and joined in the model on a SKU
column. They needed to count values in a click-throughs column from the Clicks table,
grouped by a column from the other (joined) table. They were unsure how to achieve this
grouping across the related tables.

[The user shared a screenshot in the thread]

## My Solution

This is a directional answer -- no code block was provided. Two approaches were suggested:

1. **Power Query**: Use the built-in "Group By" transformation to aggregate rows before
   loading the data into the model. This is ideal when the grouping is a permanent,
   fixed part of the data shape.

2. **DAX**: Build a virtual grouped table at report time using `SUMMARIZE()`. This keeps
   the raw data intact and lets you define the grouping dynamically in a measure or
   calculated table.

## Why It Works

The two approaches solve the same problem at different layers. Power Query Group By
collapses rows during the ETL step -- useful when you always want pre-aggregated data.
SUMMARIZE() creates a virtual table inside a DAX expression, grouping by any columns
you specify and computing aggregations row by row -- useful when you need the grouping
to be dynamic or context-sensitive (e.g., driven by slicer selections).

## Alternate Solutions

None in the thread. Single-response thread. Marked my own answer as solution on 2026-10-17
-- the thread is approximately 5 years old with no further activity from the user, so
self-marking closes it out.

## PBIX File

none
