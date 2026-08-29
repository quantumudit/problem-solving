---
platform: leetcode
problem_id: "0011"
slug: container_with_most_water
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [two_pointers]
date_solved: 2026-06-23
revisit: true
---

## Approach

Two pointers from opposite ends. At each step:

- Compute area: `min(height[l], height[r]) * (r - l)`
- Update the running max
- Move the pointer at the shorter wall inward

---

## Key Insight -- Move the Shorter Wall

Area is always bottlenecked by the shorter wall. So ask:

> "Can moving the taller wall ever increase the area?"

No. Moving the taller wall:
- Width decreases by 1
- Height is still limited by the shorter wall (or could only get shorter)
- Area can only stay the same or decrease

Moving the shorter wall is the only move that has any chance of finding a taller wall
and compensating for the width loss. So the shorter side always moves.

---

## Equal Heights

When `height[l] == height[r]`, moving either pointer is valid -- neither side is the
"bottleneck" over the other. Both solutions handle this correctly:

- `solution.py`: moves both (`l += 1`, `r -= 1`) -- explicit 3-branch logic
- `solution_v2.py`: folds equal into `<=`, so `l` advances -- compact 2-branch logic

Both are correct. v2 is the canonical form seen in interviews.

---

## Comparison

| | solution.py | solution_v2.py |
|---|---|---|
| Branches | 3 (l>r, l<r, equal) | 2 (l<=r, l>r) |
| Equal case | move both pointers | move l only |
| Speed | ~10-15ms faster empirically | standard |
| Style | explicit | canonical |

Reference: https://www.youtube.com/watch?v=UuiTKBwPgAo
