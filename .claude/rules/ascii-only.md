# Script Writing Constraints

## Plain ASCII Only

All scripts, config files, code, and markdown files must use plain ASCII characters only.
No Unicode, no special symbols, no characters outside the standard keyboard.

## Prohibited Characters

| Banned | Description              | Use instead                        |
|--------|--------------------------|------------------------------------|
| --     | Em dash (U+2014)         | - or --                            |
| -      | En dash (U+2013)         | -                                  |
| " "    | Curly double quotes      | "                                  |
| ' '    | Curly single quotes      | '                                  |
| *      | Bullet point (U+2022)    | - or *                             |
| ...    | Ellipsis (U+2026)        | ...                                |
| (c)(r) | Copyright/TM symbols     | (c) (r) (tm)                       |
| box    | Box drawing (U+2500-257F)| - or = or | (except in ASCII art)  |
| (any)  | Any Unicode > U+007F     | ASCII equivalent                   |

(Note: the table above uses ASCII replacements in the Banned column to avoid self-referential violations.)

## Separators and Dividers

Use only plain keyboard characters for visual separators:

```
# Good
# -------------------------------------------------------
# =====================================================

# Bad - box drawing characters
# -  <- U+2501
# =  <- U+2550
```

## String Content

- Use straight double quotes `"` for strings
- Use straight single quotes `'` where required by syntax
- Never use curly/smart quotes inside string content
- Use `-` for hyphens in text, not em dash or en dash

## Comments

- Use `#` for single-line comments
- Plain words and ASCII punctuation only
- No emoji in comments
- No Unicode arrows -- use `->` instead
- No Unicode checkmarks, crosses, or bullets

## Applies To

All files in this repo:
- Python (.py)
- SQL (.sql)
- Power Query (.pq)
- YAML (.yml, .yaml)
- JSON (.json, .jsonc)
- Markdown (.md)
- Shell scripts (.sh, .bash, .ps1)
- Config files of any kind

## Exceptions

- **Code blocks**: content inside fenced code blocks (` ``` `) or inline code (`` ` ``) is exempt
- **ASCII art**: directory trees, flowcharts, and box-drawing borders used for diagrams are exempt
- **notes.md section heading**: the `## Tricks / New Learnings` section in notes.md files
  uses an emoji as part of the defined template in this repo's conventions -- this specific
  heading is exempt
