---
community: microsoft_fabric
sno: "0004"
category: desktop
slug: relationship_breaks_date_link
topic_url: https://community.fabric.microsoft.com/t5/Desktop/When-creating-a-relationship-data-is-no-longer-linked-to-a-date/m-p/3831501#M1237384
date_answered: 2024-04-11
accepted: true
language: [pq]
topics: [data_model, relationships, one_to_one_relationship, merge_queries]
---

## Problem

The user created a 1:1 relationship between the date columns of two tables so they could
show data from both tables in a single graph. After creating the relationship, one table's
data was no longer correctly linked to dates in the visual.

[OP attached a screenshot of the graph showing the broken date linkage]

## My Solution

The 1:1 relationship was the root cause -- 1:1 relationships in Power BI are almost never
necessary and cause ambiguous filter propagation. The better approach is to merge the two
tables into a single flat table in Power Query, then build the visual from that one table.

Microsoft has a dedicated guidance page on this pattern:
"One-to-one relationship guidance - Power BI | Microsoft Learn"

## Why It Works

A 1:1 relationship means every row in Table A matches exactly one row in Table B and vice
versa -- which means the tables hold complementary data about the same entity and should
simply be one table. When kept separate, Power BI must resolve filter direction ambiguity
across the relationship, which causes visuals to lose the date context for one side.
Merging in Power Query produces a single, unambiguous fact table that any visual can
slice by date without relationship overhead.

## Alternate Solutions

None in the thread. OP confirmed the merge approach resolved the issue.

## PBIX File

none
