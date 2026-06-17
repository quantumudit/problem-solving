---
platform: alteryx_community
problem_id: "0015"
slug: retail_therapy
difficulty: easy
link: https://community.alteryx.com/t5/Weekly-Challenge/Challenge-164-Retail-Therapy/td-p/414754
dataset: provided
---

# Retail Therapy

## Problem
[Alteryx Community - Challenge 164: Retail Therapy](https://community.alteryx.com/t5/Weekly-Challenge/Challenge-164-Retail-Therapy/td-p/414754)

## Problem Statement
Determine the items of clothing that have the highest average rating.

The analysis must:
- Include only items with at least 10 positive feedback reviews
- Return the top 5 highest rated clothing items from each class

## Dataset

| File | Description |
|---|---|
| `data/womens_clothing_ecom_reviews.csv` | Women's clothing e-commerce reviews with ratings, feedback counts, and class labels |

## Steps

1. Filter to items with at least 10 positive feedback reviews
2. Calculate the average rating per clothing item
3. Rank items within each class by average rating
4. Return the top 5 per class

## Concepts Covered
- Data analysis
- Data preparation
- Filtering with aggregate conditions
- Grouped ranking / top-N per group
