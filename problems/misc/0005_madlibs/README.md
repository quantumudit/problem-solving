---
platform: misc
problem_id: "0005"
slug: madlibs
difficulty: null
link: ""
dataset: none
---

# Mad Libs

An interactive Mad Libs game that prompts the user to supply words for named
placeholders in a story template, then displays the completed story with the
filled-in words highlighted using Rich styling.

## Part 1 -- templates.py

### Story Templates

A `TEMPLATES` dict mapping a short name to a format-string template with named
placeholders. Four templates are included:

| Story     | Placeholders                                               |
|-----------|------------------------------------------------------------|
| adventure | adjective, name, noun, place, animal, verb, number, emotion|
| office    | adjective, name, noun, verb, number, food, emotion, adverb |
| space     | name, adjective, place, verb, animal, number, noun, emotion|
| cooking   | name, adjective, place, food, adverb, number, noun, emotion|

A placeholder name that appears more than once in a template (e.g. `{name}`) is
prompted for only once and reused across all occurrences.

### get_placeholders(template: str) -> list[str]

Extracts all unique placeholder names from a template string in order of first
appearance. Uses `re.findall(r"\{(\w+)\}", template)` and deduplicates while
preserving order.

```python
get_placeholders("Hi {name}, you have {number} messages, {name}.")
# ["name", "number"]
```

### fill_madlib(template: str, words: dict[str, str]) -> str

Fills a template string with the provided substitution dict using `str.format_map()`.

```python
fill_madlib("A {adjective} {noun}.", {"adjective": "brave", "noun": "knight"})
# "A brave knight."
```

Because `format_map` treats dict values as plain strings, passing values that contain
Rich markup works transparently -- the markup is substituted in and rendered when the
result is printed.

---

## Part 2 -- solution.py

```
python solution.py play [--story STORY_NAME]
python solution.py list
```

### play

- If `--story` is omitted, picks a template at random and tells the user which
  story was chosen.
- Validates `--story` against `TEMPLATES` and exits with an error if unknown.
- Displays a startup panel showing the story name and its placeholder list.
- Prompts the user for each placeholder in order. The article ("a" or "an") is
  chosen automatically based on the placeholder name:
  - "Enter an adjective", "Enter an adverb", "Enter an emotion"
  - "Enter a noun", "Enter a verb", "Enter a place"
- Re-prompts on empty input until a non-empty value is provided.
- Wraps each filled word in `[bold cyan]...[/bold cyan]` before substitution so
  the user-supplied words are visually highlighted in the final story.
- Displays the completed story in a green Rich panel with the story name as the title.

### list

Displays a Rich table of all available story names and their placeholder lists,
so the user knows what to expect before playing.

| Story     | Placeholders                                    |
|-----------|-------------------------------------------------|
| adventure | adjective, name, noun, place, animal, ...       |
| office    | adjective, name, noun, verb, number, food, ...  |
| ...       | ...                                             |
