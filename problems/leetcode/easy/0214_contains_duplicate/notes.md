---
platform: leetcode
problem_id: "0217"
slug: contains_duplicate
difficulty: easy
difficulty_rating: easy
language: [python]
topics: [hash_map, sets]
date_solved: 2026-06-19
revisit: false
---

## Learning

Three approaches in increasing order of conciseness, each O(n) time and O(n) space.

### solution.py -- Hashmap with early exit

Track each element's frequency in a dictionary. Return `True` the moment any count exceeds 1.

```python
for num in nums:
    count[num] = count.get(num, 0) + 1
    if count[num] > 1:
        return True
return False
```

The early exit matters when duplicates appear early in the array -- we avoid processing the rest.
An empty list returns `False` immediately since there is nothing to iterate.

### solution_v2.py -- Set membership check

A set stores only unique values. Before adding each element, check if it is already present.
If it is, we found a duplicate and return `True` immediately.

This is simpler than the hashmap version -- no need to track counts, just presence.

### solution_v3.py -- One-liner

```python
return len(set(nums)) != len(nums)
```

Converting the list to a set removes duplicates. If the resulting set is smaller than the
original list, at least one duplicate existed. Clean and Pythonic, but processes the entire
array -- no early exit.

## Comparison

| Approach | Data structure | Early exit | Notes |
|---|---|---|---|
| v1 (hashmap) | dict | Yes | Tracks count, exits on first count > 1 |
| v2 (set) | set | Yes | Simpler -- only checks presence, not count |
| v3 (one-liner) | set | No | Most concise; always scans full array |
