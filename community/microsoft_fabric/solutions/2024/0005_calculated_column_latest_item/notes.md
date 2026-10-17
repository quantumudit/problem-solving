---
community: microsoft_fabric
sno: "0005"
category: desktop
slug: calculated_column_latest_item
topic_url: https://community.fabric.microsoft.com/t5/Desktop/Adding-Calculated-Column-with-the-latest-Item/m-p/3831490#M1237379
date_answered: 2024-04-11
accepted: true
language: [dax]
topics: [calculated_columns, calculate, max, filter, variables]
---

## Problem

The user has a table (`Data`) with Category, Date, and Current columns. For each row they
wanted a new calculated column that returns the value of Current at the most recent date
within that row's category. They had tried several approaches but none produced the correct
result.

## My Solution

```dax
Latest Value =
VAR _currentCategory = Data[Category]
VAR _maxDate =
    CALCULATE (
        MAX ( Data[Date] ),
        FILTER ( Data, Data[Category] = _currentCategory )
    )
VAR _leastVal =
    CALCULATE (
        MAX ( Data[Current] ),
        FILTER ( Data, Data[Date] = _maxDate && Data[Category] = _currentCategory )
    )
RETURN
    _leastVal
```

Replace `Data` with the actual table name and `Data[Current]` with the column that holds
the value you want to retrieve.

Note: `_leastVal` is a misleading variable name in the original post -- it actually
retrieves the latest (max-date) value, not the smallest. The logic is correct despite
the name.

[A solution screenshot was shared in the thread]

## Why It Works

The calculation is split into two steps. First, `_maxDate` finds the most recent date
for the current row's category by filtering the entire table down to that category and
taking `MAX ( Data[Date] )`. Second, `_leastVal` uses both the category and that exact
date as filters to retrieve the corresponding Current value via `MAX` -- which works
correctly as long as each category has at most one row per date (or when ties exist,
returns the lexicographically largest value).

CALCULATE is needed because a calculated column evaluates row by row, and without it
aggregations like MAX would only see the current row rather than the full table.

## Alternate Solutions

None in the thread. The user did post a follow-up asking whether the formula could be
adapted to ignore blanks (for categories that have no data in the current year but have
data in prior years), but no further response was captured.

## PBIX File

none
