---
platform: alteryx_community
problem_id: "0014"
slug: date_parsing
difficulty: hard
link: https://community.alteryx.com/t5/Weekly-Challenge/Challenge-4-Date-Parsing/td-p/36731
dataset: provided
---

# Date Parsing

## Problem
[Alteryx Community - Challenge 4: Date Parsing](https://community.alteryx.com/t5/Weekly-Challenge/Challenge-4-Date-Parsing/td-p/36731)

## Problem Statement
The input file contains dates embedded in text fields, represented in multiple inconsistent
formats. Parse each date string and produce a clean, uniform Date/Time field.

## Input Date Formats

| Example | Format |
|---|---|
| `16-APR-2005` | DD-MON-YYYY |
| `Nov 16, 1900` | Mon DD, YYYY |
| `4-SEP-00` | D-MON-YY |
| `Jan 5 2000` | Mon D YYYY |

## Dataset

| File | Description |
|---|---|
| `data/date_embedded_text.csv` | Raw text fields containing dates in mixed formats |

## Steps

1. Identify the date format for each record
2. Parse the date string into a normalized Date/Time value
3. Output the original text alongside the new parsed Date/Time field

## Concepts Covered
- Data analysis
- Multi-format date parsing
- String pattern matching and extraction
