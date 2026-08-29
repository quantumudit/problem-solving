---
platform: leetcode
problem_id: "0424"
slug: longest_repeating_character_replacement
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [sliding_window, two_pointers]
date_solved: 2026-08-29
revisit: true
---

## Pattern

Variable-size sliding window. Expand right freely; shrink left when the window
becomes invalid.

## Core invariant

A window is valid when:

```
window_size - max_frequency <= k
```

- `window_size` = `right - left + 1`
- `max_frequency` = frequency of the most common character in the window
- `window_size - max_frequency` = number of characters that need to be replaced
- If that count exceeds `k`, the window is invalid

## Key insight

You always keep the most frequent character and replace everything else. So the
question becomes: can you fill the non-dominant characters with at most `k`
replacements?

This means you don't need to try every target character explicitly. Just track
the frequency of each character in the window, and the dominant one determines
validity automatically.

## Why `max(count.values())`

`count` holds the frequency of every character currently inside the window.
`max(count.values())` gives the frequency of the dominant character. Since `s`
is uppercase English letters, this is at most 26 values -- effectively O(1).

## Window shrink behavior

When the window is invalid, `left` advances by exactly one. This is intentional:
we only care about windows *longer* than the current best. There is no point
shrinking aggressively back to a smaller valid window -- it can't improve `max_len`.

## Recognition rule

"Longest substring you can make uniform with at most k replacements":
- Sliding window
- Validity check: `window_size - max_freq_in_window <= k`
- Shrink from left when invalid
