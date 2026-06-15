---
platform: misc
problem_id: "0004"
slug: regex_explorer
difficulty: null
link: ""
dataset: none
---

# Regex Explorer

A command-line text analysis tool built in two parts:

1. A `TextAnalysis` class that uses compiled regex patterns to extract special
   character positions and count characters by category.
2. A Typer CLI that takes a text argument, runs the analysis, and displays the
   results with Rich-formatted output.

## Part 1 -- TextAnalysis Class

```python
TextAnalysis(text: str)
```

All five patterns are compiled once at module level and shared across both methods.

### Methods

| Method               | Returns                  | Description                                         |
|----------------------|--------------------------|-----------------------------------------------------|
| special_chars_pos()  | list[tuple[str, int]]    | Each non-word non-whitespace char and its position  |
| char_counts()        | dict[str, int]           | Count of each character category plus total         |

### special_chars_pos()

Finds all characters matching `[^\w\s]` using `re.finditer` and returns a list of
`(matched_char, start_index)` tuples in order of appearance.

| Input                | Output                                          |
|----------------------|-------------------------------------------------|
| "Hello, World!"      | [(",", 5), ("!", 12)]                           |
| "price: $9.99"       | [(":", 5), ("$", 8), (".", 10)]                 |
| "no specials here"   | []                                              |
| "C++ is #1 lang!"    | [("+", 1), ("+", 2), ("#", 7), ("!", 14)]       |

### char_counts()

Returns a dict with counts for each character category:

```python
{
    "special_chars":     int,
    "uppercase_letters": int,
    "lowercase_letters": int,
    "whitespaces":       int,
    "digits":            int,
    "total":             int,
}
```

---

## Part 2 -- Typer CLI

```
python solution.py search "Hello, World!"
python solution.py search "C++ is #1 lang!"
```

Text is passed as a positional argument. Empty input is rejected with an error panel.

### Output

**1. Input panel** -- displays the original text with each special character
highlighted inline in bold red using Rich markup.

```
+-------------------------------+
|          Input Text           |
| Hello[bold red],[/] World[bold red]![/]  |
+-------------------------------+
```

**2. Match table** -- one row per special character found:

| Match | Index | Context                  |
|-------|-------|--------------------------|
| ,     | 5     | Hello[bold],[\] Wor      |
| !     | 12    | orld[bold]![/]           |

The Context column shows up to 3 characters on either side of the match, with the
matched character highlighted.

If no special characters are found, a styled green message is shown instead.

**3. Character counts table** -- counts per category with the Total row highlighted:

| Category           | Count |
|--------------------|-------|
| Special Characters |     2 |
| Uppercase Letters  |     2 |
| Lowercase Letters  |     8 |
| Whitespaces        |     1 |
| Digits             |     0 |
| **Total**          |    14 |
