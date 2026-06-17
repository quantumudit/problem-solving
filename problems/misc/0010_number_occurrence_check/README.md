---
platform: w3resource
problem_id: "0010"
slug: number_occurrence_check
difficulty: easy
link: https://www.w3resource.com/python-exercises/puzzles/python-programming-puzzles-1.php
dataset: none
---

# Number Occurrence Check

## Problem
[W3Resource - Number Occurrence Check](https://www.w3resource.com/python-exercises/puzzles/python-programming-puzzles-1.php)

## Problem Statement
Write a Python program to determine if a list of integers contains exactly two occurrences
of 19 and at least three occurrences of 5. Return `True` if both conditions are met,
otherwise `False`.

## Constraints
- Input is a list of integers
- Exactly two 19's required: `count(19) == 2`
- At least three 5's required: `count(5) >= 3`

## Examples

**Example 1:**
Input: `[19, 5, 19, 5, 5]`
Output: `True`

**Example 2:**
Input: `[19, 5, 19]`
Output: `False` (only two 5's, need at least three)

**Example 3:**
Input: `[5, 19, 5, 5]`
Output: `False` (only one 19, need exactly two)

**Example 4:**
Input: `[19, 19, 19, 5, 5, 5]`
Output: `False` (three 19's, need exactly two)

## Variants

| File | Approach |
|---|---|
| `solution.py` | Primary -- using built-in `count()` |
| `variations/v1_dict_frequency.py` | Dictionary frequency count |
| `variations/v2_manual_iteration.py` | Manual iteration without `count()` |
| `variations/v3_recursive.py` | Recursive verification |

### Variant Descriptions

**Primary:** Write a Python program to find a list of integers with exactly two occurrences
of nineteen and at least three occurrences of five.

**Variant 1:** Determine if a list of integers meets the condition of exactly two 19's and
three or more 5's using dictionary frequency counts. Return `True` otherwise `False`.

**Variant 2:** Determine if a list of integers meets the condition of exactly two 19's and
three or more 5's without using built-in `count()`, by iterating through the list and
tracking occurrences.

**Variant 3:** Recursively verify that a list has exactly two occurrences of 19 and at
least three occurrences of 5.
