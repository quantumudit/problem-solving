---
platform: leetcode
problem_id: "0347"
slug: top_k_frequent_elements
difficulty: medium
link: https://leetcode.com/problems/top-k-frequent-elements/
dataset: none
---

## Problem
[LeetCode - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

## Problem Statement

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.
You may return the answer in any order.

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `k` is in the range `[1, the number of unique elements in the array]`
- It is guaranteed that the answer is unique.

**Follow up:** Your algorithm's time complexity must be better than `O(n log n)`, where `n` is the array's size.

## Example

**Example 1:**

Input: `nums = [1,1,1,2,2,3], k = 2`
Output: `[1,2]`

**Example 2:**

Input: `nums = [1], k = 1`
Output: `[1]`

**Example 3:**

Input: `nums = [1,2,1,2,1,2,3,1,3,2], k = 2`
Output: `[1,2]`

## Files

- [solution.py](solution.py) -- sort by frequency (O(n log n))
- [solution_v1.py](solution_v1.py) -- bucket sort, reverse slice traversal (O(n))
- [solution_v2.py](solution_v2.py) -- bucket sort, range() countdown traversal (O(n))
- [notes.md](notes.md)
