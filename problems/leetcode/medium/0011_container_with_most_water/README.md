---
platform: leetcode
problem_id: "0011"
slug: container_with_most_water
difficulty: medium
link: https://leetcode.com/problems/container-with-most-water/
dataset: none
---

## Problem
[LeetCode - Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

## Problem Statement

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such
that the two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container that holds the most water.

Return the maximum amount of water a container can store.

Note: you may not slant the container.

## Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

## Example

**Example 1:**

Input: `height = [1,8,6,2,5,4,8,3,7]`
Output: `49`
Explanation: The max area is formed between indices 1 and 8 (heights 8 and 7).
Area = min(8,7) * (8-1) = 7 * 7 = 49.

**Example 2:**

Input: `height = [1,1]`
Output: `1`

## Files

- [solution.py](solution.py) -- two pointers, explicit 3-branch equal handling
- [solution_v2.py](solution_v2.py) -- two pointers, compact 2-branch (canonical)
- [notes.md](notes.md)
