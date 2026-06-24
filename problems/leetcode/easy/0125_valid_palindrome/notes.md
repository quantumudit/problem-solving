---
platform: leetcode
problem_id: "0125"
slug: valid_palindrome
difficulty: easy
difficulty_rating: easy
language: [python]
topics: [string_ops, two_pointers]
date_solved: 2026-06-23
revisit: true
---

## Approach

Clean the string, then compare it to its reverse.

1. Strip all non-alphanumeric characters with `re.sub()` and lowercase
2. Compare the cleaned string to its reverse slice `[::-1]`

One line of logic after the cleanup.

---

## Regex Pattern -- `[\W_]`

`\W` matches any character NOT in `[a-zA-Z0-9_]`. The problem is that `\W` does NOT match
underscore -- underscore is part of `\w`. So `[\W_]` adds it explicitly.

`[\W_]` = "match non-word characters OR underscore" -- keeps only letters and digits.

| Pattern | Matches | Effect |
|---------|---------|--------|
| `\w`    | `[a-zA-Z0-9_]` | letters, digits, underscore |
| `\W`    | anything not `\w` | strips punctuation and spaces |
| `[\W_]` | `\W` or `_`    | strips everything except letters and digits |

`re.IGNORECASE` is passed but doesn't affect the substitution -- `.lower()` handles case.
The flag is harmless here.

---

## Alternative -- Two Pointers (revisit)

The regex approach builds a new string, so space is O(n). A two-pointer approach avoids
this by checking characters in-place:

- `l, r = 0, len(s) - 1`
- skip non-alphanumeric characters on both ends
- compare `s[l].lower()` and `s[r].lower()`
- move pointers inward until they meet

This is O(1) extra space. Reference: https://youtu.be/jJXJ16kPFWg?si=6gpJ90adBdF9XxE0
