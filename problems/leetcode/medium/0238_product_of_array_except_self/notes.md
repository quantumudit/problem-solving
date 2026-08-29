---
platform: leetcode
problem_id: "0238"
slug: product_of_array_except_self
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [stateful_iteration]
date_solved: 2026-06-23
revisit: true
---

## Approach

Build two arrays -- `prefix` and `suffix` -- then multiply them element-wise.

- `prefix[i]` = product of all elements strictly to the LEFT of index `i`
- `suffix[i]` = product of all elements strictly to the RIGHT of index `i`
- `result[i] = prefix[i] * suffix[i]`

Both arrays start as all 1s. `prefix[0] = 1` (nothing to the left of index 0).
`suffix[n-1] = 1` (nothing to the right of the last index).

Step-by-step on `nums = [1,2,3,4]`:

| i | nums[i] | prefix[i] | suffix[i] | result[i] |
|---|---------|-----------|-----------|-----------|
| 0 | 1       | 1         | 24        | 24        |
| 1 | 2       | 1         | 12        | 12        |
| 2 | 3       | 2         | 4         | 8         |
| 3 | 4       | 6         | 1         | 6         |

---

## Why No Division

The naive approach divides the total product by each element, but that breaks when any
element is 0. The prefix/suffix approach avoids division entirely and handles zeros naturally.

---

## Space Complexity Issue (revisit)

`solution.py` uses two extra O(n) arrays (`prefix` and `suffix`), so space is O(n).

The follow-up asks for O(1) extra space. This is achievable by reusing the output array:
1. First pass (left to right): build prefix products directly into `result`
2. Second pass (right to left): multiply a running `suffix` variable into `result` in-place

```python
result = [1] * n
for i in range(1, n):
    result[i] = result[i-1] * nums[i-1]  # prefix pass into output

suffix = 1
for i in range(n-1, -1, -1):
    result[i] *= suffix                    # fold suffix in-place
    suffix *= nums[i]
```

`result` itself holds the prefix, so no separate `prefix` array is needed.
`suffix` is a single integer -- O(1) extra space.
