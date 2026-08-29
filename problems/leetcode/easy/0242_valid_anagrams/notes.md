---
platform: leetcode
problem_id: "0242"
slug: valid_anagram
difficulty: easy
difficulty_rating: easy
language: [python]
topics: [hash_map, string_ops]
date_solved: 2026-06-19
revisit: false
---

## Learning

An anagram has identical character frequencies. The task reduces to: build a frequency map for
each string and compare them.

### solution.py -- Dual frequency map (single loop)

Rather than two separate loops, build both character-frequency maps in one pass. This works
because both strings must be the same length to be anagrams, so index `i` is always valid
for both.

```python
for i in range(len(s)):
    s_count[s[i]] = s_count.get(s[i], 0) + 1
    t_count[t[i]] = t_count.get(t[i], 0) + 1
return s_count == t_count
```

The `.get(key, 0)` pattern initialises a missing key to zero instead of raising a `KeyError`.

Early length check (`if len(s) == len(t)`) avoids any computation when sizes differ -- two
strings of different lengths can never be anagrams.

### solution_v2.py -- Counter

`Counter` from `collections` counts element frequencies in a single call:

```python
from collections import Counter

Counter("anagram")
# Counter({'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1})
```

Comparing two `Counter` objects directly checks that every character appears the same number
of times in both strings. Concise and readable, but relies on a library -- the manual approach
in v1 is more appropriate in a pure DSA interview setting.

## Comparison

| Approach | Method | Library dependency |
|---|---|---|
| v1 | Manual dual frequency map, single loop | None |
| v2 | Counter comparison | collections |
