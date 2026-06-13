---
platform: misc
problem_id: "0004"
slug: regex_explorer
difficulty: null
link: ""
dataset: none
---

# Regex Explorer

A command-line tool that searches input text for characters that are
neither word characters (\w) nor whitespace (\s) -- that is, punctuation
and special symbols. Each match is reported with its position, and the
original text is displayed with matches highlighted using Rich markup.

## Function to Implement

### match_special_chars(text: str) -> list[tuple[str, int]]

Search the input string for all non-word, non-whitespace characters using
a compiled regex pattern and return a list of (matched_char, start_index)
tuples in order of appearance.

- Pattern: `[^\w\s]`
- Input: a string
- Output: list of (str, int) tuples

| Input                   | Output                                  |
|-------------------------|-----------------------------------------|
| "Hello, World!"         | [(",", 5), ("!", 12)]                   |
| "price: $9.99"          | [(":", 5), ("$", 8), (".", 10)]         |
| "no specials here"      | []                                      |
| "C++ is #1 lang!"       | [("+", 2), ("#", 7), ("!", 15)] |

## CLI Interface

Accept the text to search as a Typer argument.

```
python solution.py search "Hello, World!"
python solution.py search "C++ is #1 lang!"
```

### Output Format

1. Display the original text with each matched character highlighted
   inline using Rich markup (e.g., bold or colored span).
2. Below that, display a Rich table with three columns:
   - Match : the matched character
   - Index : its position in the string (0-based)
   - Context : a short excerpt showing a few characters around the match

If no matches are found, display a styled message indicating a clean result.
