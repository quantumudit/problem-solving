---
community: microsoft_fabric
sno: "0002"
category: desktop
slug: percentage_completed_of_tasks_created
topic_url: https://community.fabric.microsoft.com/t5/Desktop/Percentage-completed-of-tasks-created/m-p/3831797#M1237454
date_answered: 2024-04-12
accepted: true
language: [dax]
topics: [calculated_measures, divide, count, aggregations]
---

## Problem

The user wanted to calculate the percentage of completed tasks out of total requested tasks
for a selected month (via a slicer), and display the result in a column or visual.
They shared a screenshot of their data but provided limited context about the data model
structure.

## My Solution

```dax
Percentage Completed by Requested =
DIVIDE ( COUNT ( Table['Completed'] ), COUNT ( Table['Requested'] ) )
```

Replace `Table['Completed']` and `Table['Requested']` with the actual table and column
names from your data model. Format the measure as a percentage in the visual formatting
options.

## Why It Works

`COUNT` tallies non-blank values in the specified column, so it effectively counts rows
where that date field is populated. `DIVIDE` performs safe division -- it returns BLANK
instead of an error when the denominator is zero, which is the correct behaviour for a
percentage measure that may have months with no requests.

## Alternate Solutions

None in the thread. Single-answer thread, marked as solution by the poster.

## PBIX File

none
