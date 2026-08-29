---
platform: leetcode
problem_id: "0424"
slug: longest_repeating_character_replacement
difficulty: medium
link: https://leetcode.com/problems/longest-repeating-character-replacement/
dataset: none
---

## Problem
[LeetCode - Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)

## Problem Statement

You are given a string `s` and an integer `k`. You can choose any character of the string and
change it to any other uppercase English character. You can perform this operation at most `k`
times.

Return the length of the longest substring containing the same letter you can get after
performing the above operations.

## Constraints

- `1 <= s.length <= 10^5`
- `s` consists of only uppercase English letters.
- `0 <= k <= s.length`

## Example

**Example 1:**

Input: `s = "ABAB", k = 2`
Output: `4`
Explanation: Replace the two 'A's with two 'B's or vice versa.

**Example 2:**

Input: `s = "AABABBA", k = 1`
Output: `4`
Explanation: Replace the 'A' in the middle with 'B' to form `"AABBBBA"`. The substring `"BBBB"`
has the longest repeating letters, giving length 4.

## Files

- [solution.py](solution.py)
- [notes.md](notes.md)
