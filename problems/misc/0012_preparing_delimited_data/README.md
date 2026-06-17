---
platform: alteryx_community
problem_id: "0012"
slug: preparing_delimited_data
difficulty: easy
link: https://community.alteryx.com/t5/Weekly-Challenge/Challenge-2-Preparing-Delimited-Data/td-p/36622
dataset: provided
---

# Preparing Delimited Data

## Problem
[Alteryx Community - Challenge 2: Preparing Delimited Data](https://community.alteryx.com/t5/Weekly-Challenge/Challenge-2-Preparing-Delimited-Data/td-p/36622)

## Problem Statement
The input file contains two different delimiters -- double quotes and single quotes -- that
surround different data types. Strip out both delimiters and format the data cleanly.

## Dataset

| File | Description |
|---|---|
| `data/poems.csv` | Raw input with mixed quote delimiters surrounding field values |

## Steps

1. Identify fields wrapped in double quotes and fields wrapped in single quotes
2. Strip the quote characters from the field values
3. Output the cleaned, consistently formatted data

## Concepts Covered
- Data preparation
- String parsing and delimiter stripping
- Mixed-format text handling
