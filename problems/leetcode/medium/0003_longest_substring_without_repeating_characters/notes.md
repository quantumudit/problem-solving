---
platform: leetcode
problem_id: "0003"
slug: longest_substring_without_repeating_characters
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [sliding_window, two_pointers]
date_solved: 2026-08-29
revisit: true
---

## What you got right

You immediately recognized:
- Sliding Window
- Two pointers (left, right)
- Need a set for fast duplicate detection

That means your pattern recognition is improving.

## Where you got stuck

### Mistake 1: Restarting the window

You did something like:

```
left = right
vals = set()
length = 1
```

Your thinking was: "I found a duplicate, so I'll start over."

The problem is that you threw away useful information.

Example: `abcade`
When the second `a` appears, you restarted.
But the valid window should become `bca`, not `a`.

### Mistake 2: Set and window became inconsistent

At many points, `vals` did not represent `s[left:right+1]`.
Once those two go out of sync, the algorithm becomes unreliable.

## Biggest lesson

The invariant is: the set must always contain exactly the characters inside the current window.

Whenever that invariant breaks: shrink the window until it becomes valid again. Not restart.

## Recognition rule

Whenever you see "Longest/Shortest substring satisfying a condition":

```
Expand right
  -> Window invalid?
     -> Shrink left until valid
        -> Update answer
```
