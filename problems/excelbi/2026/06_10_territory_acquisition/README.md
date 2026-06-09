---
platform: excelbi
problem_id: "PQ00397"
slug: territory_acquisition
difficulty: null
link: https://lnkd.in/gywHUGik
dataset: provided
---

## Problem
[ExcelBI - Territory Acquisition Simulation](https://lnkd.in/gywHUGik)

## Problem Statement

You are given monthly revenue data for a set of territories.

Initially, each territory is owned by itself.

For each month, perform the following steps:

1. Identify the territory with the highest revenue for that month.
2. Identify the territory with the lowest revenue for that month.
3. The owner of the highest-revenue territory acquires ownership of the lowest-revenue territory.
4. Once a territory is acquired:
   - It is no longer considered an independent territory.
   - Its ownership is permanently transferred to the acquiring owner.
   - It continues to generate revenue in future months under the new owner.
5. Ownership changes take effect from the next month onward.
6. Repeat the process for each month in chronological order.

## Important Notes

- Acquisition decisions are based solely on the individual revenue of each territory for the current month.
- Ownership does not influence future acquisition decisions.
- Revenues from multiple owned territories must not be combined when determining the highest- or lowest-revenue territory.
- A territory's revenue remains associated with that territory regardless of its owner.
- Once a territory is acquired, it cannot be acquired again.
- Continue processing until the final month and return the final ownership structure.

## Constraints


## Examples

Input:

| Month | Territory | Revenue |
|-------|-----------|--------:|
| Jan   | North     | 120     |
| Jan   | South     | 95      |
| Jan   | East      | 140     |
| Jan   | West      | 80      |
| Feb   | North     | 150     |
| Feb   | South     | 60      |
| Feb   | East      | 130     |
| Feb   | West      | 70      |
| Mar   | North     | 160     |
| Mar   | South     | 50      |
| Mar   | East      | 120     |
| Mar   | West      | 75      |
| Apr   | North     | 170     |
| Apr   | South     | 45      |
| Apr   | East      | 110     |
| Apr   | West      | 72      |
| May   | North     | 180     |
| May   | South     | 40      |
| May   | East      | 115     |
| May   | West      | 70      |
| Jun   | North     | 190     |
| Jun   | South     | 35      |
| Jun   | East      | 118     |
| Jun   | West      | 68      |

Output:
