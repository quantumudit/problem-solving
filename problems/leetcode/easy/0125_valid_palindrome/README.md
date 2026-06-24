---
platform: leetcode
problem_id: "0125"
slug: valid_palindrome
difficulty: easy
link: https://leetcode.com/problems/valid-palindrome/
dataset: none
---

## Problem
[LeetCode - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)

## Problem Statement

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and
removing all non-alphanumeric characters, it reads the same forward and backward.
Alphanumeric characters include letters and numbers.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

## Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

## Example

**Example 1:**

Input: `s = "A man, a plan, a canal: Panama"`
Output: `true`
Explanation: `"amanaplanacanalpanama"` is a palindrome.

**Example 2:**

Input: `s = "race a car"`
Output: `false`
Explanation: `"raceacar"` is not a palindrome.

**Example 3:**

Input: `s = " "`
Output: `true`
Explanation: `s` is an empty string after removing non-alphanumeric characters.
An empty string reads the same forward and backward.

## Files

- [solution.py](solution.py)
- [notes.md](notes.md)
