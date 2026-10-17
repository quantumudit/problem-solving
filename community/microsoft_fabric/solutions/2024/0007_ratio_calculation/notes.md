---
community: microsoft_fabric
sno: "0007"
category: dax_commands_and_tips
slug: ratio_calculation
topic_url: https://community.fabric.microsoft.com/t5/DAX-Commands-and-Tips/Ratio-Calculation/m-p/3834715#M149935
date_answered: 2024-04-12
accepted: true
language: [dax]
topics: [calculated_measures, divide, calculate, filter, selectedvalue, all]
---

## Problem

The user had a table (`MainTable`) with three columns: ClientID, Sub Account, and Amount.
A single ClientID could have multiple sub-accounts, each with its own amount. They needed
a measure that returned the ratio of each sub-account's amount to the total amount for
its parent ClientID -- so the denominator had to be scoped to the ClientID, not the
entire table.

[The user shared a screenshot in the thread]

## My Solution

```dax
Ratio =
VAR _clientTotal =
    CALCULATE (
        SUM ( MainTable[Amount] ),
        FILTER (
            ALL ( MainTable ),
            MainTable[ClientID] = SELECTEDVALUE ( MainTable[ClientID] )
        )
    )
VAR _ratio =
    DIVIDE ( SUM ( MainTable[Amount] ), _clientTotal )
RETURN
    _ratio
```

Replace `MainTable` with the actual table name and `MainTable[Amount]`,
`MainTable[ClientID]` with the appropriate column names.

Optionally, the `SUM ( MainTable[Amount] )` in the numerator can be replaced with a
reusable base measure:

```dax
Total Amount = SUM ( MainTable[Amount] )
```

[A solution screenshot was shared in the thread]

## Why It Works

In a visual or table, the current filter context already narrows `SUM ( MainTable[Amount] )`
to the sub-account row being evaluated -- giving the numerator automatically. The challenge
is the denominator, which must ignore the sub-account filter while keeping only the ClientID
filter. `ALL ( MainTable )` wipes every filter on the table, and the `FILTER` then re-applies
just the ClientID condition using `SELECTEDVALUE` to capture which ClientID is currently in
context. `DIVIDE` handles the zero-denominator edge case cleanly.

## Alternate Solutions

None in the thread.

## PBIX File

none
