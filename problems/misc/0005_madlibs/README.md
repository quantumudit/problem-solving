---
platform: misc
problem_id: "0005"
slug: madlibs
difficulty: null
link: ""
dataset: none
---

# Mad Libs

An interactive Mad Libs game that prompts the user to supply words for
named placeholders in a story template, then displays the completed
story with Rich styling.

## What to Implement

### Story Templates

Include at least three distinct templates, each identified by a short
name (e.g. "adventure", "office", "space"). Each template is a Python
f-string-style string with named placeholders such as {noun}, {verb},
{adjective}, {place}, {emotion}.

Example template:

```
One {adjective} day, a {noun} decided to {verb} all the way to {place}.
Everyone in town was {emotion} to see it happen.
```

Placeholder names should be descriptive (noun, verb, adjective, adverb,
place, name, number, emotion, animal, food -- use whatever fits the story).

### fill_madlib(template: str, words: dict[str, str]) -> str

Fill a template string with the provided substitution dict.

- Input: a template string, a dict mapping placeholder names to words
- Output: the completed story string with all placeholders replaced

### Typer CLI

```
python solution.py play [--story STORY_NAME]
python solution.py list
```

#### play

- If `--story` is omitted, select a template at random.
- Extract all placeholder names from the chosen template.
- Prompt the user interactively for each placeholder using Typer's
  prompt() -- e.g. "Enter a noun: ".
- After all words are collected, pass them to `fill_madlib()` and
  display the completed story in a Rich panel with styled text.
- The story title (template name) appears as the panel header.

#### list

Display a Rich table listing all available story names and their
placeholder words, so the user knows what to expect before playing.

### Input Validation

If the user provides an empty string for any placeholder, prompt again
until a non-empty value is entered.
