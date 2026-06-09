---
name: new-problem
description: Scaffold a new problem -- confirms slug and branch name with user, creates folder, README.md, and notes.md. No solution files. All git actions require explicit user approval.
argument-hint: "[platform] [slug]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(mkdir *) Bash(ls *) Write Edit Read
---

Today's date: !`date +%Y-%m-%d`

Scaffold a new problem. Follow the steps below in order. Never skip ahead.
Every git action requires explicit user approval before running.

---

### Step 1 -- Deduce and confirm the slug

From the problem description or $ARGUMENTS, derive a snake_case slug.
Show the user: "Proposed slug: `{slug}` -- does that look good?"
Wait for confirmation or correction before proceeding.

---

### Step 2 -- Collect missing problem metadata

Check what information is already known from the problem description. Ask only for what is missing:

1. **Platform**: `leetcode` | `stratascratch` | `excelbi` | `edna` | `challenges`
2. **Problem link**: direct URL to the problem
3. **Difficulty**: `easy` | `medium` | `hard` -- leetcode and stratascratch only; `null` for others
4. **Difficulty rating**: personal assessment -- `easy` | `medium` | `hard` | `null`; ask for all platforms
5. **Problem ID**:
   - leetcode / stratascratch: numeric, zero-padded to 4 digits e.g. `"0001"`
   - excelbi: series prefix + 5-digit padded (7 chars total):
     `PQ` for Power Query e.g. `"PQ00398"`, `EX` for Excel e.g. `"EX00991"`
   - edna / challenges: omit
6. **Language(s)**: `python` | `sql` | `pq` -- can be multiple.
   For Python, also ask: **which library?** `none` | `pandas` | `polars` | `duckdb` | `pyspark` | other.
   Use `none` for pure DSA (no external library).
7. **Date**: defaults to today's date injected above

For `challenges`, also collect:
- Source (e.g. `data_with_danny`)
- Challenge name (snake_case)
- Question number (e.g. `01`)

Ask for missing fields in one go if possible. Do not ask for fields already provided.

---

### Step 3 -- Confirm branch name

Derive the branch name from the confirmed slug and collected metadata:

| Platform | Branch pattern |
|---|---|
| leetcode | `leetcode/{difficulty}/{id}_{slug}` |
| stratascratch | `stratascratch/{difficulty}/{id}_{slug}` |
| excelbi | `excelbi/{YYYY_MM_DD}_{slug}` |
| edna | `edna/{YYYY_w##}_{slug}` |
| challenges | `challenges/{source}/{challenge_name}` |

Show the user: "Proposed branch: `{branch_name}` -- OK to create?"
Wait for explicit approval. Do not create the branch until the user confirms.

---

### Step 4 -- Create branch and folder

Only after user approves the branch name, show the exact commands and ask permission:

```
git checkout main
git checkout -b {branch_name}
mkdir -p {folder_path}
```

Folder path patterns:

| Platform | Folder path |
|---|---|
| leetcode | `problems/leetcode/{difficulty}/{id}_{slug}/` |
| stratascratch | `problems/stratascratch/{difficulty}/{id}_{slug}/` |
| excelbi | `problems/excelbi/{YYYY}/{MM_DD_slug}/` |
| edna | `problems/edna/{YYYY}/{w##_slug}/` |
| challenges question | `problems/challenges/{source}/{challenge}/{q##_slug}/` |

---

### Step 5 -- Create README.md

For standalone problems (leetcode, stratascratch, excelbi, edna), create at `{folder_path}/README.md`:

```markdown
---
platform: {platform}
problem_id: "{id}"
slug: {slug}
difficulty: {difficulty}
link: {link}
dataset: none
---

## Problem
[{Platform} - {Title}]({link})

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
link: {link}
dataset:
date_started: {date}
date_completed: null
---

## Challenge
[{Source} - {Challenge Title}]({link})

## Description


## Dataset Overview


## Questions Index
| # | Slug | Language | Date Solved |
|---|------|----------|-------------|
| q{##} | {slug} | {language} | {date} |
```

If the problem statement was provided in full, fill in the Problem Statement, Constraints, and Examples sections now. Otherwise leave them blank for the user to fill in.

---

### Step 6 -- Create notes.md

For standalone problems, create at `{folder_path}/notes.md`:

```markdown
---
platform: {platform}
problem_id: "{id}"
slug: {slug}
difficulty: {difficulty}
difficulty_rating: {difficulty_rating}
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


## Tricks / New Learnings


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


## Tricks / New Learnings

```

**`notes.md` language field** -- use the library name, not `python`, when a library is used:
```yaml
language: [pandas]          # not [python]
language: [pandas, polars]  # multiple library solutions
language: [python]          # pure DSA only
```

No solution files are created at this stage. The user will create them when ready to solve.

---

### Step 7 -- Commit with user approval

Show the user the exact command and ask permission before running:

```
git add {folder_path}
git commit -m "wip: scaffold {slug}"
```

Wait for explicit approval. Do not commit until the user confirms.

---

### Step 8 -- Push with user approval

Show the user the exact command and ask permission before running:

```
git push -u origin {branch_name}
```

Wait for explicit approval. Do not push until the user confirms.

---

After everything is done, confirm what was created and remind the user to fill in
any blank sections in README.md (problem statement, constraints, examples, link).
