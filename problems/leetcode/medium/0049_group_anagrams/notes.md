---
platform: leetcode
problem_id: "0049"
slug: group_anagrams
difficulty: medium
difficulty_rating: medium
language: [python]
topics: [hash_map, string_ops]
date_solved: 2026-06-19
revisit: false
---

## Learning

The core idea: two words are anagrams if and only if they share the same "signature" -- a
canonical representation of their character frequencies. Build a hashmap keyed by that
signature; all anagram groups collect under the same key automatically.

The three solutions differ in how they build the signature.

---

### solution.py -- Sorted frequency string

Build a character-frequency dict for each word, then serialize it into a sorted string like
`"a1e1t1"`. Words with identical character counts produce identical keys.

Works correctly but has two costs: building the freq dict for every word, and sorting the
dict items to ensure a consistent key ordering.

---

### solution_v2.py -- 26-element count tuple

Replace the sorted string with a fixed-length tuple of 26 counts -- one slot per letter.

```python
signature = [0] * 26
for char in word:
    signature[ord(char) - ord("a")] += 1
key = tuple(signature)
```

`ord(char) - ord('a')` maps each letter to an index 0-25:
- `'a'` -> `ord('a') - ord('a')` = 0
- `'e'` -> `ord('e') - ord('a')` = 4
- `'z'` -> `ord('z') - ord('a')` = 25

Example with `"eat"`:

| Step | char | index | count at index |
|---|---|---|---|
| 1 | 'e' | 4 | count[4] = 1 |
| 2 | 'a' | 0 | count[0] = 1 |
| 3 | 't' | 19 | count[19] = 1 |

`"eat"` and `"tea"` produce the same tuple because they contain the same letters -- the order
of processing does not matter, only the final counts.

The list is converted to a tuple before use as a dict key because:

> To be a dict key, a value must be **hashable** and **immutable**. Tuples qualify; lists do not.

This approach avoids sorting entirely, which makes it faster than v1 for long words.

---

### solution_v3.py -- defaultdict (cleanest version)

Same 26-element count tuple as v2, but uses `defaultdict(list)` from `collections`:

```python
from collections import defaultdict

anagrams = defaultdict(list)
anagrams[tuple(signature)].append(word)
```

`defaultdict(list)` auto-initialises a missing key to an empty list, so we can call
`.append()` directly without checking whether the key exists first. This removes the
`anagrams.get(key, []) + [word]` pattern from v2 and is both faster and more readable.

## Comparison

| Approach | Signature type | Key building | Library |
|---|---|---|---|
| v1 | Sorted freq string | dict + sort | None |
| v2 | 26-element tuple | count array | None |
| v3 | 26-element tuple | count array | collections |

v3 is the fastest and cleanest -- no sorting, no `.get()` fallback, direct `.append()`.
