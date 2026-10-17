---
community: microsoft_fabric
sno: "0003"
category: desktop
slug: average_of_monthly_averages
topic_url: https://community.fabric.microsoft.com/t5/Desktop/How-to-calculate-average-of-monthly-averages/m-p/3831790#M1237452
date_answered: 2024-04-12
accepted: false
language: [dax]
topics: [calculated_measures, sumx, summarize, addcolumns, distinctcount, isinscope, divide]
---

## Problem

The user tracks OT hours worked by employees (Date, Name, Hours). In a Matrix visual,
they wanted to show per-month averages defined as total OT hours for the month divided
by the count of unique employees who worked OT that month -- not a simple row count.
Their existing measures (`OTHours`, `UniqueEmps`, `OTAvg`) worked correctly for individual
months, but the Matrix grand total column applied `OTAvg` to the entire dataset (dividing
total hours by total unique employees across all months = 68/4 = 17), rather than computing
the average of the three monthly averages (5 + 8 + 7 = 20, divided by 3 = 6.67).

[OP attached two screenshots showing the Matrix visual and the incorrect grand total behaviour]

## My Solution

```dax
OT Hours Average =
VAR _otHours =
    SUM ( OTHOURS[Hours] )
VAR _uniqueEmp =
    DISTINCTCOUNT ( OTHOURS[Name] )
VAR _otAvg =
    DIVIDE ( _otHours, _uniqueEmp )
VAR _months =
    DISTINCTCOUNT ( OTHOURS[Month] )
VAR _totalOTAvg =
    SUMX (
        ADDCOLUMNS (
            SUMMARIZE (
                OTHOURS,
                OTHOURS[Month],
                "emp", DISTINCTCOUNT ( OTHOURS[Name] ),
                "hrs", SUM ( OTHOURS[Hours] )
            ),
            "avg_hrs", DIVIDE ( [hrs], [emp] )
        ),
        [avg_hrs]
    )
VAR _yearAvg =
    DIVIDE ( _totalOTAvg, _months )
RETURN
    IF ( ISINSCOPE ( OTHOURS[Month] ), _otAvg, _yearAvg )
```

A calculated column is needed to get the month-end date from the raw Date column (skip
if a Month column already exists):

```dax
Month = EOMONTH ( OTHOURS[Date], 0 )
```

Replace `OTHOURS` with the actual table name in your model.

## Why It Works

`ISINSCOPE ( OTHOURS[Month] )` is the key: it returns TRUE when the measure is being
evaluated inside a month column cell, and FALSE at the grand total level. This lets the
single measure behave differently depending on where it appears in the Matrix.

At the month level it returns `_otAvg` (standard per-month calculation). At the grand
total level it builds a virtual per-month table with `SUMMARIZE`, adds a per-month average
column with `ADDCOLUMNS`, sums those averages with `SUMX`, and divides by the count of
distinct months -- producing the average-of-averages rather than the naive total/total
calculation the default subtotal would apply.

## Alternate Solutions

`jgeddes` posted a simpler approach using `SUMMARIZE` and `AVERAGEX`, which was marked
as the accepted solution by the OP:

```dax
Average of Average =
VAR _vTable =
    SUMMARIZE (
        OTHours,
        OTHours[Date].[Month],
        "__average", [OTAvg]
    )
RETURN
    AVERAGEX ( _vTable, [__average] )
```

This is more concise -- `AVERAGEX` over a summarized table handles the averaging directly
without needing `ISINSCOPE` or explicit month counting.

## PBIX File

none
