---
platform: leetcode
problem_id: "0167"
slug: two_sum_ii_input_array_is_sorted
difficulty: medium
difficulty_rating: easy
language: [python]
topics: [two_pointers]
date_solved: 2026-06-23
revisit: true
---

## Approach

Two pointers starting at opposite ends. Because the array is sorted:

- `numbers[l] + numbers[r] < target` -- sum too small, move `l` right to increase it
- `numbers[l] + numbers[r] > target` -- sum too large, move `r` left to decrease it
- equal -- found the pair, return 1-indexed positions

Sorted order guarantees each move strictly changes the sum in the right direction,
so the loop always terminates and never needs to backtrack.

---

## Why Not a Hash Map

Two Sum I (unsorted) needs a hash map because there is no structure to exploit.
Here the array is sorted, so two pointers give O(n) time with O(1) extra space --
the constraint the problem explicitly requires.

|          | Two Sum I | Two Sum II   |
| -------- | --------- | ------------ |
| Input    | unsorted  | sorted       |
| Strategy | hash map  | two pointers |
| Time     | O(n)      | O(n)         |
| Space    | O(n)      | O(1)         |

---

## Why the Loop Bound Works

The loop runs at most `n` times. Since exactly one solution is guaranteed, the `else`
branch always fires before the loop exhausts. The `for` bound just prevents an infinite
loop -- the function always returns early via the `else`.

Reference: https://www.youtube.com/watch?v=cQ1Oz4ckceM
