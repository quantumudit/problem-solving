---
platform: leetcode
problem_id: "0567"
slug: permutation_in_string
difficulty: medium
link: https://leetcode.com/problems/permutation-in-string/
dataset: none
---

## Problem
[LeetCode - Permutation in String](https://leetcode.com/problems/permutation-in-string/)

## Problem Statement

Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`,
or `false` otherwise.

In other words, return `true` if one of `s1`'s permutations is a substring of `s2`.

## Constraints

- `1 <= s1.length, s2.length <= 10^4`
- `s1` and `s2` consist of lowercase English letters.

## Example

**Example 1:**

Input: `s1 = "ab", s2 = "eidbaooo"`
Output: `true`
Explanation: `s2` contains one permutation of `s1` (`"ba"`).

**Example 2:**

Input: `s1 = "ab", s2 = "eidboaoo"`
Output: `false`

## Files

| File | Approach | Time |
|---|---|---|
| [solution.py](solution.py) | Brute force: rebuild window map each step | O(n * k) |
| [solution_v3.py](solution_v3.py) | Dict sliding window: slide properly | O(n) |
| [solution_v2.py](solution_v2.py) | Array + matches counter: avoid full comparison | O(n) |

- [notes.md](notes.md)
