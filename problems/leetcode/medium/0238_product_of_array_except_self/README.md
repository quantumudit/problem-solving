---
platform: leetcode
problem_id: "0238"
slug: product_of_array_except_self
difficulty: medium
link: https://leetcode.com/problems/product-of-array-except-self/
dataset: none
---

## Problem
[LeetCode - Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)

## Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the
product of all the elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in `O(n)` time and without using the division operation.

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The input is generated such that `answer[i]` is guaranteed to fit in a 32-bit integer.

**Follow up:** Can you solve the problem in `O(1)` extra space complexity? (The output array does
not count as extra space for space complexity analysis.)

## Example

**Example 1:**

Input: `nums = [1,2,3,4]`
Output: `[24,12,8,6]`

**Example 2:**

Input: `nums = [-1,1,0,-3,3]`
Output: `[0,0,9,0,0]`

## Files

- [solution.py](solution.py) -- prefix and suffix product arrays (O(n) space)
- [notes.md](notes.md)
