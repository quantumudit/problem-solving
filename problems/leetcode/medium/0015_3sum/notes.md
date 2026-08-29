---
platform: leetcode
problem_id: "0015"
slug: 3sum
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [two_pointers, sorting]
date_solved: 2026-06-23
revisit: true
---

## Approach

Sort the array, then fix one element and reduce the problem to Two Sum II:

1. Sort `nums`
2. For each index `i`, set `l = i+1`, `r = n-1`
3. Run two pointers inward until `l >= r`
4. Collect all triplets that sum to zero; skip duplicates

Two solutions -- same core algorithm, different dedup strategies.

---

## Solution Comparison

| | solution.py | solution_v2.py |
|---|---|---|
| Dedup method | `set` of tuples | skip equal neighbors inline |
| Loop construct | `for _ in range(...)` bounded | `while l < r` |
| Output build | convert set to list at end | append directly to list |
| Performance | slower (1953 ms, ~6th percentile) | faster |
| Clarity | simpler to write first | canonical interview pattern |

---

## Why `while l < r`, Not `for _ in range(...)`

In solution.py the inner loop is `for _ in range(i+1, len(nums))`. This bounds the
iteration count but the variable is never used -- `l` and `r` are what actually move.

The idiomatic pattern for two pointers is `while l < r` because the pointers ARE the
loop condition. The `for` variant works but obscures the intent.

Rule of thumb: if the loop body only moves `l` or `r`, use `while l < r`.

---

## Duplicate Handling

Two places where duplicates must be skipped in solution_v2.py:

**1. Duplicate anchor (outer loop):**
```python
if i > 0 and nums[i] == nums[i - 1]:
    continue
```
If the anchor value was already processed, skip it. This prevents the entire two-pointer
pass from running again on the same fixed value.

**2. Duplicate pointers (after a match):**
```python
while l < r and nums[l] == nums[l - 1]:
    l += 1
while l < r and nums[r] == nums[r + 1]:
    r -= 1
```
After recording a triplet, advance both pointers past any equal neighbors so the same
triplet is not added again.

Without either of these, `[0,0,0,0]` would produce `[[0,0,0],[0,0,0]]`.

---

## Pattern Recognition Checklist

Before coding a sum/combination problem, ask:

1. Can sorting help?
2. Can I fix one element and reduce the problem? (4Sum -> 3Sum -> 2Sum)
3. Are unique answers required? If yes -- how will I skip duplicates?
4. Can the search space shrink from both ends? If yes -- two pointers.

Reference: https://www.youtube.com/watch?v=jzZsG8n2R9A
