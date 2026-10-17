---
community: microsoft_fabric
sno: "0009"
category: dax_commands_and_tips
slug: weekly_yoy_cumulative_totals
topic_url: https://community.fabric.microsoft.com/t5/DAX-Commands-and-Tips/Weekly-year-over-year-cumulative-totals-when-weeks-start-on/m-p/3833321#M149896
date_answered: 2024-04-12
accepted: true
language: [dax]
topics: [calculated_measures, calculated_columns, countrows, filter, all, selectedvalue, year]
---

## Problem

The user had a ticket purchases table with a date column. The 2023 and 2024 data started
on different calendar dates, making a direct date-to-date YoY comparison impossible. To
align the two years, the user added week numbers to each row and wanted a cumulative count
of ticket purchases by week that could be compared across years.

[The user shared a screenshot of the data structure in the thread]

## My Solution

First, a calculated column to extract the year from the date:

```dax
Year = YEAR ( 'Table'[date] )
```

Then a measure for the cumulative count up to the current week within the current year:

```dax
Cumulative Count =
COUNTROWS (
    FILTER (
        ALL ( 'Table' ),
        'Table'[Week] <= MAX ( 'Table'[Week] )
            && 'Table'[Year] = MAX ( 'Table'[Year] )
    )
)
```

Replace `'Table'` with the actual table name.

[A solution screenshot was shared in the thread]

## Why It Works

Because the two years have different start dates, week numbers are used as the alignment
axis instead of calendar dates. `ALL ( 'Table' )` lifts all filters from the table so
every row is visible. The FILTER then re-applies two conditions: keep only rows whose
Week is at most the current filter context's MAX week (giving the cumulative up to that
point) and whose Year matches the current MAX year (isolating one year at a time). COUNTROWS on that
filtered set produces the running total. Dropping this measure into a visual sliced by
Year lets both years accumulate from their own Week 1, making them directly comparable.

## Alternate Solutions

None in the thread.

## PBIX File

none
