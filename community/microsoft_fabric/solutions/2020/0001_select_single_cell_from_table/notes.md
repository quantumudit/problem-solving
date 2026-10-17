---
community: microsoft_fabric
sno: "0001"
category: dax_commands_and_tips
slug: select_single_cell_from_table
topic_url: https://community.fabric.microsoft.com/t5/DAX-Commands-and-Tips/Select-single-cell-from-table-to-another-table/m-p/1399492#M25732
date_answered: 2020-09-28
accepted: true
language: [dax]
topics: [calculated_columns, filter, lookupvalue, containsstring]
---

## Problem

The user downloads a quarterly file that always has the same structure. One specific cell
contains the period label (e.g., "2018 Q3"). They wanted to pull that single cell value into
a column in a new Power BI table.

Their attempt used `SELECTCOLUMNS` with `CONTAINS`, but it returned `TRUE` instead of the
actual period string.

## My Solution

```dax
Period =
VAR Tab =
    FILTER(
        ALL('Table'[Column1]),
        CONTAINSSTRING('Table'[Column1], "Q1") ||
        CONTAINSSTRING('Table'[Column1], "Q2") ||
        CONTAINSSTRING('Table'[Column1], "Q3") ||
        CONTAINSSTRING('Table'[Column1], "Q4")
    )
RETURN
    LOOKUPVALUE('Table'[Column1], 'Table'[Column1], Tab)
```

This is a calculated column formula. Replace `'Table'[Column1]` with the actual table and
column name that holds the raw data from the quarterly file.

## Why It Works

- `ALL('Table'[Column1])` scans the full column ignoring any filter context
- `FILTER` narrows it to the single row whose value contains a quarter identifier
- `LOOKUPVALUE` retrieves the actual text of that row rather than a boolean

The original attempt failed because `CONTAINS` checks for existence and returns TRUE/FALSE --
it does not return the matched value.

## Alternate Solutions

None in the thread. Single-answer thread, solution accepted by OP.

## PBIX File

none
