---
community: microsoft_fabric
sno: "0008"
category: dax_commands_and_tips
slug: repairs_per_hour
topic_url: https://community.fabric.microsoft.com/t5/DAX-Commands-and-Tips/Need-help-with-repairs-per-hour/m-p/3832850#M149879
date_answered: 2024-04-12
accepted: true
language: [dax]
topics: [calculated_columns, calculated_measures, datediff, count, divide, sum]
---

## Problem

The user had a `Repairs` table with a Work Order column, an Owner column, and two datetime
columns: Created On and Completed On. They wanted a measure that calculated the number of
repairs completed per hour, broken down by owner, but could not figure out how to derive
the rate from those timestamps.

## My Solution

First, a calculated column to capture each repair's duration in minutes:

```dax
Duration = DATEDIFF ( Repairs[Created on], Repairs[Completed On], MINUTE )
```

Then a measure that converts the per-minute rate to an hourly figure:

```dax
Repairs per Hour =
VAR _repairPerMinute = DIVIDE ( COUNT ( Repairs[Work Order] ), SUM ( Repairs[Duration] ) )
VAR _repairPerHour = _repairPerMinute * 60
RETURN
    ROUND ( _repairPerHour, 0 )
```

Replace `Repairs` with the actual table name and adjust column names to match.

[A solution screenshot was shared in the thread]

## Why It Works

The rate is calculated as: number of repairs / total minutes spent = repairs per minute,
then multiplied by 60 to convert to repairs per hour. `COUNT ( Repairs[Work Order] )`
counts the rows (i.e., individual repairs) in the current filter context -- which means
slicing by Owner in a visual will automatically scope both the count and the duration sum
to that owner. `DIVIDE` handles the case where the total duration is zero. `ROUND` removes
the decimal since a fractional repair count per hour is not meaningful here.

## Alternate Solutions

None in the thread.

## PBIX File

none
