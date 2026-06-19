---
platform: leetcode
problem_id: "0049"
slug: group_anagrams
difficulty: medium
link: https://leetcode.com/problems/group-anagrams/
dataset: none
---

## Problem
[LeetCode - Group Anagrams](https://leetcode.com/problems/group-anagrams/)

## Problem Statement

Given an array of strings `strs`, group all anagrams together and return the groups in any order.

## Constraints

- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.

## Example

**Example 1:**

Input: `strs = ["eat","tea","tan","ate","nat","bat"]`
Output: `[["bat"],["nat","tan"],["ate","eat","tea"]]`
Explanation: `"eat"`, `"tea"`, and `"ate"` are anagrams. `"nat"` and `"tan"` are anagrams.
`"bat"` has no anagram partners.

**Example 2:**

Input: `strs = [""]`
Output: `[[""]]`

**Example 3:**

Input: `strs = ["a"]`
Output: `[["a"]]`

## Files

- [solution.py](solution.py)
- [solution_v2.py](solution_v2.py)
- [solution_v3.py](solution_v3.py)
- [notes.md](notes.md)
