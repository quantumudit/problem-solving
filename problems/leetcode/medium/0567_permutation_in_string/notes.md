---
platform: leetcode
problem_id: "0567"
slug: permutation_in_string
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [sliding_window]
date_solved: 2026-08-29
revisit: true
---

## What you got right

You immediately recognized:
- Window size never changes
- Need frequency counts
- Fixed-size sliding window

Pattern recognition is solid.

## Where you got stuck

Your first solution rebuilt the frequency map on every window step:

```python
for every window position:
    s2_map = {}
    for i in range(lo, hi):
        s2_map[s2[i]] = ...
```

It worked, but O(n * k) because the inner loop runs `len(s1)` times per step.

## What you learned

A sliding window should slide, not rebuild.

Instead of: destroy old window -> build new window

Think: remove one character + add one character. That's all.

## Three solutions

**solution.py** -- brute force

Rebuilds s2's frequency map from scratch at every step. O(n * k).

**solution_v3.py** -- clean dict sliding window

Slides properly: add incoming char, remove outgoing char, delete key when count
hits 0. Dict comparison (`window == s1_count`) on every step. O(n) time.

**solution_v2.py** -- optimal (array + matches counter)

Uses fixed-size arrays of 26 instead of dicts. Maintains a `matches` counter
tracking how many character frequencies agree between s1 and the current window.
When `matches == 26`, the window is a permutation.

Key insight: instead of comparing two full arrays on every step, track a single
integer. Increment or decrement `matches` surgically when adding or removing a
character changes whether that character's count agrees. O(n) time, best constant.

## Biggest lesson

For fixed-size windows:

1. Build the initial window
2. Slide: add incoming character, remove outgoing character
3. Check answer

Never rebuild.
