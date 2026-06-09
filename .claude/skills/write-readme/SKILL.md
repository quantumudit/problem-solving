---
name: write-readme
description: Generate or fill in the per-problem README.md from the problem statement. Use after scaffolding a problem when you have the problem statement ready to paste.
argument-hint: "[paste problem statement, or leave empty to be prompted]"
disable-model-invocation: true
allowed-tools: Read Glob Write
---

## Context

Current branch: !`git branch --show-current`

---

Generate or fill in README.md for the current problem.
If $ARGUMENTS contains the problem statement, use it directly.
Otherwise ask the user: "Please paste the problem statement."

Read ONLY files inside the problem-specific folder identified in Step 1.
Do not read files outside that folder.

---

## Step 1 -- Identify the problem folder and README type

Parse the branch name to derive all values:

| Branch | Folder | README type |
|---|---|---|
| `leetcode/{difficulty}/{id}_{slug}` | `problems/leetcode/{difficulty}/{id}_{slug}/` | standalone |
| `stratascratch/{difficulty}/{id}_{slug}` | `problems/stratascratch/{difficulty}/{id}_{slug}/` | standalone |
| `excelbi/{YYYY_MM_DD}_{slug}` | `problems/excelbi/{YYYY}/{MM_DD_slug}/` | standalone |
| `edna/{YYYY_w##}_{slug}` | `problems/edna/{YYYY}/{w##_slug}/` | standalone |
| `challenges/{source}/{challenge}` | `problems/challenges/{source}/{challenge}/` | challenge-level |

**Derived frontmatter values:**

| Branch segment | Frontmatter field | Notes |
|---|---|---|
| `leetcode` / `stratascratch` / etc. | `platform` | as-is |
| `{difficulty}` | `difficulty` | easy / medium / hard / null |
| `{id}` | `problem_id` | leetcode/stratascratch: zero-padded e.g. `"0001"`; excelbi: prefix + 4-digit e.g. `"PQ00398"`; omit for challenges/edna |
| `{slug}` | `slug` | as-is from branch |

If the branch is `main` or unrecognized, stop and ask the user which problem to document.

---

## Step 2 -- Inspect the problem folder

Use Glob to list all files in the problem folder.

- If `README.md` already exists, read it.
  - If it has a real problem statement (not placeholder text), ask the user:
    "README.md already has content -- do you want to overwrite it or update specific sections?"
  - If it is a skeleton from `/new-problem` (empty statement, placeholder link), fill it in.
- If no `README.md` exists, create one from scratch.
- If solution file(s) exist, read them briefly -- the data structures and function
  signatures hint at input/output types, which helps parse the problem statement correctly.
  Do not use solution content to infer the problem statement itself.

**Inventory files for the `## Files` section.** Note which of the following are present:
- Solution files: `solution.py`, `solution.sql`, `solution.pq`, `solution_v2.py`, etc.
- Data files: anything under `data/` (CSV, Excel, SQL seed files, etc.)
- `notes.md` (may not exist yet -- only link if present)

Only link files that actually exist. Do not create placeholder links.

**Challenge branches only:** README.md lives at the challenge root
(`problems/challenges/{source}/{challenge}/README.md`), not inside question folders.
Individual question folders (`q01_slug/`, `q02_slug/`) do not have README.md files.
If the user asks to document a specific question, write or update the Questions Index
table in the challenge-level README instead.

---

## Step 3 -- Get the problem statement

If $ARGUMENTS is non-empty, treat it as the full problem statement.
Otherwise ask the user to paste it.

Once you have the problem statement, extract:

| Field | Where to find it |
|---|---|
| Title | Usually the first line or heading |
| Statement body | Main description paragraph(s) |
| Output columns | Named output fields the problem asks you to compute (e.g. CurrentStage, Status) |
| Input schema | Column names and types if described; otherwise infer from data file if present |
| Constraints | Usually a bullet list under "Constraints" or "Notes" |
| Examples | Input/output pairs, often labelled "Example 1", "Example 2", etc. |
| Link | URL in the pasted text, or ask the user: "What is the link to this problem?" |
| Dataset | For excelbi/edna: note the data file referenced. For others: `none` unless a file was attached. |

If a section has no content (e.g. no constraints listed), omit that section entirely --
do not leave blank stubs.

---

## Step 4 -- Generate the README.md

### Standalone problems (leetcode, stratascratch, excelbi, edna)

```markdown
---
platform: {platform}
problem_id: "{id}"
slug: {slug}
difficulty: {difficulty}
link: {link}
dataset: {dataset}
---

## Problem
[{Platform} - {Title}]({link})

## Problem Statement
{one or two sentences of prose giving context -- what the dataset represents and what
needs to be computed. Then, if the problem defines multiple named output columns, present
them as a table:}

| Output Column | Description |
|---|---|
| ColumnName | Full description including edge-case values (e.g. "Not Started" if none cleared) |

## Input Schema
{include this section only when dataset != none}
{column-level table derived from the problem statement or the data file:}

| Column | Type | Description |
|---|---|---|
| ColName | type | description |

{add a plain-text note for any structural quirks, e.g. "Not all cases have all stages
in the dataset." or "One row per employee per month."}

## Constraints
{bullet list only if constraints are explicitly stated in the problem -- omit this section entirely if none}

## Example
{use markdown tables for tabular input/output -- bold-label each block:}

**Input{qualifier if needed, e.g. "(selected rows)"}:**

| Col1 | Col2 | ... |
|---|---|---|
| val | val | ... |

**Expected output{qualifier if needed}:**

| Col1 | Col2 | ... |
|---|---|---|
| val | val | ... |

{follow the tables with one sentence explaining any non-obvious case shown in the example,
especially edge cases like out-of-order completions, nulls, or boundary values}

## Files
{relative links to all files that exist -- solution file(s) first, then data/, then notes.md}
- [solution.py](solution.py)
- [data/filename.csv](data/filename.csv)
- [notes.md](notes.md)

## Source
{excelbi / edna only -- omit for leetcode / stratascratch which have no external post}
- [{Source or Author} - {Post or Challenge Name}]({full_url}) -- {context e.g. "PQ_Challenge_398, posted YYYY-MM-DD"}
```

- Omit `problem_id` from the frontmatter for `challenges` and `edna` (no ID).
- For `excelbi`, include `problem_id` using the series prefix and 5-digit padded number
  (7 chars total): `PQ` for Power Query challenges e.g. `"PQ00398"`, `EX` for Excel
  challenges e.g. `"EX00991"`.
- Set `difficulty: null` for excelbi, edna, and challenges.
- Omit `## Source` for leetcode and stratascratch -- the `link` frontmatter field
  is sufficient and there is no associated LinkedIn/external post to credit.
- Omit `## Files` entries for files that do not yet exist (e.g. `notes.md` before
  it has been created).
- Omit `## Input Schema` when `dataset: none`.
- Omit `## Constraints` entirely when none are stated -- do not leave a blank stub.

### Challenge-level README (challenges branch)

```markdown
---
platform: challenges
source: {source}
challenge: {challenge}
link: {link}
dataset: {dataset filename or description}
date_started: {today YYYY-MM-DD}
date_completed: null
---

## Challenge
[{Source} - {Challenge Title}]({link})

## Description
{description from problem statement}

## Dataset Overview
{tables, schema, or data description -- leave blank if not yet known}

## Questions Index
| # | Slug | Language | Date Solved |
|---|------|----------|-------------|
| q01 | {first_question_slug} | {language} | {date or leave blank} |
```

If a challenge README already exists and the user is adding a new question,
append a row to the Questions Index table only -- do not modify other sections.

---

## Step 5 -- Confirm and write

Show the complete README.md content to the user before writing.
Ask: "Does this look correct? I will write it to {path}."

After confirmation, write the file using the Write tool.
Report the file path written.

Do not update notes.md -- that is the user's responsibility.
