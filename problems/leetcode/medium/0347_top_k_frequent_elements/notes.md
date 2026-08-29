---
platform: leetcode
problem_id: "0347"
slug: top_k_frequent_elements
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [hash_map, sorting, bucket_sort]
date_solved: 2026-06-23
revisit: false
---

## Approach

Three solutions, two distinct strategies:

- `solution.py`: frequency map + sort by count. Clean and readable but O(n log n) -- violates the follow-up constraint.
- `solution_v1.py` / `solution_v2.py`: bucket sort. O(n) time. Both use the same core logic; v2 uses `range()` countdown instead of a reverse slice.

---

## Key Insight -- Bucket Sort

The maximum frequency any element can have is `len(nums)` (all elements are the same).
That gives a fixed upper bound, so we can use the frequency itself as an array index.

Build `buckets` of size `len(nums) + 1`:
- `buckets[f]` holds all numbers that appear exactly `f` times
- Index 0 is unused (no element has zero frequency)

Iterate from the highest index down, collecting elements until we have `k`.

Step-by-step on `nums = [1,1,1,2,2,3], k = 2`:

| Step | Action | State |
|---|---|---|
| Count | {1:3, 2:2, 3:1} | frequency map built |
| Bucket | buckets[3]=[1], buckets[2]=[2], buckets[1]=[3] | placed by frequency |
| Collect | i=5..4 empty, i=3 -> add 1 | result=[1] |
| Collect | i=2 -> add 2, len==k | return [1,2] |

---

## Gotcha -- List of Lists

`[[]] * n` creates `n` references to the SAME list object -- mutating one mutates all.

```python
# wrong
buckets = [[]] * (len(nums) + 1)
buckets[1].append(99)   # appends to every slot

# correct
buckets = [[] for _ in range(len(nums) + 1)]
buckets[1].append(99)   # only slot 1 is affected
```

---

## Comparison

| | solution.py | solution_v1.py | solution_v2.py |
|---|---|---|---|
| Strategy | sort by frequency | bucket sort | bucket sort |
| Time | O(n log n) | O(n) | O(n) |
| Space | O(n) | O(n) | O(n) |
| Traversal | sorted() + slice | reverse slice [::-1] | range() countdown |
| Follow-up | fails | passes | passes |

v1 and v2 are functionally identical. v2 uses `range(len-1, 0, -1)`, which is more
explicit about the direction; v1 uses `[::-1]`, which is more Pythonic but hides the index.
