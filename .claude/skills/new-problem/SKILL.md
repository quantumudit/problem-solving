---
name: new-problem
description: Scaffold a new problem — creates the branch, folder structure, README.md, notes.md, and empty solution file. Use when starting work on a new problem on any supported platform.
argument-hint: "[platform] [slug]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(mkdir *) Bash(ls *)
---

Today's date: !`date +%Y-%m-%d`

Scaffold a new problem. If $ARGUMENTS was provided, parse platform and slug from it; otherwise ask the user for the missing pieces one at a time.

### Inputs to collect

1. **Platform**: `leetcode` | `stratascratch` | `excelbi` | `edna` | `challenges`
2. **Difficulty**: `easy` | `medium` | `hard` — leetcode and stratascratch only; use `null` for others
3. **Problem ID**: numeric, zero-padded to 4 digits (e.g. `"0001"`) — leetcode and stratascratch only; omit for others
4. **Slug**: snake_case (e.g. `two_sum`)
5. **Language(s)**: `python` | `sql` | `pq` — can be multiple.
   For Python, also ask: **which library?** `none` | `pandas` | `polars` | `duckdb` | `pyspark` | other.
   Use `none` for pure DSA (no external library). This determines the solution filename and
   the `language` field in `notes.md`.
6. **Date solved**: defaults to today's date injected above

For `challenges`, also collect:
- Source (e.g. `data_with_danny`)
- Challenge name (snake_case)
- Question number (e.g. `01`)

---

### Step 1 — Determine branch name

| Platform | Branch pattern |
|---|---|
| leetcode | `leetcode/{difficulty}/{id}_{slug}` |
| stratascratch | `stratascratch/{difficulty}/{id}_{slug}` |
| excelbi | `excelbi/{YYYY_MM_DD}_{slug}` |
| edna | `edna/{YYYY_w##}_{slug}` |
| challenges | `challenges/{source}/{challenge_name}` |

### Step 2 — Determine folder path

| Platform | Folder path |
|---|---|
| leetcode | `problems/leetcode/{difficulty}/{id}_{slug}/` |
| stratascratch | `problems/stratascratch/{difficulty}/{id}_{slug}/` |
| excelbi | `problems/excelbi/{YYYY}/{MM_DD_slug}/` |
| edna | `problems/edna/{YYYY}/{w##_slug}/` |
| challenges question | `problems/challenges/{source}/{challenge}/{q##_slug}/` |

### Step 3 — Create branch and folder

```bash
git checkout main
git checkout -b {branch_name}
mkdir -p {folder_path}
```

### Step 4 — Create README.md

For standalone problems (leetcode, stratascratch, excelbi, edna), create at `{folder_path}/README.md`:

```markdown
---
platform: {platform}
problem_id: "{id}"
slug: {slug}
difficulty: {difficulty}
link:
dataset: none
---

## Problem
[{Platform} - {Title}]()

## Problem Statement


## Constraints


## Examples
Input:
Output:
```

For `challenges`, create a challenge-level README at `problems/challenges/{source}/{challenge}/README.md`:

```markdown
---
platform: challenges
source: {source}
challenge: {challenge}
link:
dataset:
date_started: {date}
date_completed: null
---

## Challenge
[{Source} - {Challenge Title}]()

## Description


## Dataset Overview


## Questions Index
| # | Slug | Language | Date Solved |
|---|------|----------|-------------|
| q{##} | {slug} | {language} | {date} |
```

### Step 5 — Create notes.md

For standalone problems, create at `{folder_path}/notes.md`:

```markdown
---
platform: {platform}
problem_id: "{id}"
slug: {slug}
difficulty: {difficulty}
language: [{language}]
topics: []
date_solved: {date}
revisit: false
---

## Approach


## Complexity
- Time:
- Space:

## What tripped me up


## 💡 Tricks / New Learnings


## Revisit notes

```

For challenge questions, create at `{q_folder}/notes.md` (no frontmatter `problem_id`):

```markdown
---
platform: challenges
slug: {slug}
difficulty: null
language: [{language}]
topics: []
date_solved: {date}
revisit: false
---

## Approach


## Complexity
- Time:
- Space:

## What tripped me up


## 💡 Tricks / New Learnings

```

### Step 6 — Create empty solution file

| Language | Library | File |
|---|---|---|
| python | none (pure DSA) | `solution.py` |
| python | pandas | `solution_pandas.py` |
| python | polars | `solution_polars.py` |
| python | duckdb | `solution_duckdb.py` |
| python | pyspark | `solution_pyspark.py` |
| python | other | `solution_{library}.py` |
| sql | -- | `solution.sql` |
| pq | -- | `solution.pq` |

For challenges, place the solution file inside the question folder (`q##_slug/`).
For multiple languages or libraries, create one file per language/library combination.

**`notes.md` language field** -- use the library name, not `python`, when a library is used:
```yaml
language: [pandas]          # not [python]
language: [pandas, polars]  # multiple library solutions
language: [python]          # pure DSA only
```

---

### Step 7 -- Push branch to remote

Push the branch immediately so it exists on remote from the start:

```bash
git push -u origin {branch_name}
```

If the push fails (e.g. no remote configured), report the error clearly -- do not
leave this step silently skipped.

---

After scaffolding, confirm the files created, the remote push, and remind the user
to fill in the problem link and statement in README.md.
