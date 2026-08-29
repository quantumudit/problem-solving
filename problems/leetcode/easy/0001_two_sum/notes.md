---
platform: leetcode
problem_id: "0001"
slug: two_sum
difficulty: easy
difficulty_rating: easy
language: [python]
topics: [hash_map]
date_solved: 2026-06-19
revisit: false
---

## Learning

The key insight is: for each number, compute its complement (`target - num`) and check if that
complement has already been seen in previous iterations.

We build the hashmap on the fly -- store each number's index as we go. When we find a complement
already in the map, we have our pair and can return immediately.

```python
seen = {}
for i in range(len(nums)):
    complement = target - nums[i]
    if complement in seen:
        return [i, seen[complement]]
    seen[nums[i]] = i
```

This avoids the brute-force O(n^2) nested loop by trading space for time:

| Approach | Time | Space |
|---|---|---|
| Brute force (nested loops) | O(n^2) | O(1) |
| Hash map (one pass) | O(n) | O(n) |

The single-pass approach works because we check for the complement before storing the current
number. This handles the case where the same element appears twice (e.g. `[3,3], target=6`) --
we never pair a number with itself because its index isn't in the map yet when we check.
