---
platform: leetcode
problem_id: "0015"
slug: 3sum
difficulty: medium
link: https://leetcode.com/problems/3sum/
dataset: none
---

## Problem
[LeetCode - 3Sum](https://leetcode.com/problems/3sum/)

## Problem Statement

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that
`i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

The solution set must not contain duplicate triplets.

## Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

## Example

**Example 1:**

Input: `nums = [-1,0,1,2,-1,-4]`
Output: `[[-1,-1,2],[-1,0,1]]`
Explanation: The distinct triplets that sum to zero are `[-1,-1,2]` and `[-1,0,1]`.

**Example 2:**

Input: `nums = [0,1,1]`
Output: `[]`
Explanation: No triplet sums to zero.

**Example 3:**

Input: `nums = [0,0,0]`
Output: `[[0,0,0]]`

## Files

- [solution.py](solution.py) -- two pointers + set dedup
- [solution_v2.py](solution_v2.py) -- two pointers + inline duplicate skipping (canonical)
- [notes.md](notes.md)
