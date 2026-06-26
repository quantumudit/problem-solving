---
platform: w3resource
problem_id: "0010"
slug: number_occurrence_check
difficulty: easy
difficulty_rating: easy
language: [python]
topics: [conditional_logic, stateful_iteration, recursion]
date_solved: 2026-06-18
revisit: false
---

## Approach
The primary solution uses Python's built-in `list.count()` -- two calls, one per target value,
combined into a single boolean expression. Clean and readable.

The three variants each explore a different way to build the same frequency check:
- v1 builds a frequency dictionary with `dict.get()` to avoid KeyError on first encounter
- v2 iterates once and tracks named counters (`count_19`, `count_5`) using a `match` statement
- v3 recurses head-first through the list, carrying counts as accumulator arguments with
  an early exit when `count_19` exceeds 2

## Complexity
- Time: O(n) -- all variants scan the list once; `solution.py` scans twice (two `count()` calls)
- Space: O(1) for solution.py, v2, v3 -- O(k) for v1 where k is the number of distinct values

## What tripped me up
Nothing significant. The recursive approach needs care around the base case: the final
condition is checked only when the list is exhausted, not mid-traversal -- except for the
early exit on `count_19 > 2` which prunes unnecessary recursion.

## Tricks / New Learnings
`dict.get(key, default)` is the idiomatic way to count occurrences without pre-initializing
the dictionary -- avoids the boilerplate of checking `if key not in freq` before incrementing.

Python's `match` statement (3.10+) reads more clearly than a chain of `if/elif` when
dispatching on a single value with no binding needed.

Recursive accumulators passed as default arguments (`count_19: int = 0`) keep the public
signature clean -- the caller never needs to pass the initial state.

## Variations
- v1_dict_frequency -- frequency dictionary with dict.get(); O(k) space vs O(1) for others
- v2_manual_iteration -- single-pass with named counters and match statement; no built-ins used
- v3_recursive -- head recursion with accumulator args; early exits when count_19 exceeds 2

## Revisit notes
Not needed -- all four approaches are clean and the tradeoffs are well understood.
