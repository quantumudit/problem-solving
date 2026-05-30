---
name: queue-problem
description: Create a GitHub issue to log a problem found online for solving later. Use when you want to save a problem to the backlog without starting it now.
argument-hint: "[paste problem details or statement]"
disable-model-invocation: true
allowed-tools: Bash(gh *)
---

Collect the problem details below, then create a GitHub issue using the backlog template.
If $ARGUMENTS contains a problem statement or details, use them to pre-fill the fields.

---

## Step 1 -- Collect problem details

Ask for each field that is missing. Do not ask for all fields at once -- gather them
one group at a time so the user is not overwhelmed.

**Required:**
- **Platform**: snake_case name of the source platform (e.g. `leetcode`, `stratascratch`, `excelbi`, `edna`, `challenges`, or any other)
- **Slug**: snake_case problem name (e.g. `two_sum`, `sales_by_region`)
- **Link**: direct URL to the problem

**Platform-specific:**
- `leetcode` / `stratascratch`: **Problem ID** (zero-padded to 4 digits) and **Difficulty** (`easy` | `medium` | `hard`)
- `excelbi`: **Date** in `YYYY_MM_DD` format
- `edna`: **Week** in `YYYY_w##` format
- `challenges`: **Source** (e.g. `data_with_danny`) and **Challenge name**

**Optional (skip if not available yet):**
- Problem statement
- Constraints
- Examples
- Initial notes or approach ideas

---

## Step 2 -- Detect target repo

Run:
```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

If this succeeds, use the returned `owner/repo` value.
If it fails (not a git repo yet), ask the user:
"What is the GitHub repo for this project? (format: owner/repo)"

Store the repo as `{repo}` for use in all subsequent `gh` commands.

---

## Step 3 -- Ensure labels exist

Create only the labels needed for this specific issue (`--force` skips errors on existing):

```bash
gh label create "backlog" --color "0075ca" --description "Problem queued for later" --force --repo {repo}
gh label create "{platform}" --color "e4e669" --description "" --force --repo {repo}
```

If the problem has a difficulty (easy/medium/hard), also create:
```bash
gh label create "{difficulty}" --color "{color}" --description "" --force --repo {repo}
```

Difficulty colors: `easy` = `0e8a16`, `medium` = `e4a010`, `hard` = `b60205`.

If any label creation fails, note it but continue -- missing labels are non-blocking.

---

## Step 4 -- Format issue title and body

**Title format:**

Use the pattern that best fits the platform:

| Has numeric ID + difficulty | Has date/week ref | Has source/challenge hierarchy | Generic |
|---|---|---|---|
| `[{platform}] {id} {slug} [{difficulty}]` | `[{platform}] {date_or_week} {slug}` | `[{platform}] {source} {challenge}` | `[{platform}] {slug}` |

Examples:
- `[leetcode] 0042 trapping_rain_water [hard]`
- `[hackerrank] 0017 climbing_the_leaderboard [medium]`
- `[excelbi] 2025_04_01 sales_by_region`
- `[challenges] data_with_danny murder_mystery`
- `[projecteuler] 0001 multiples_of_3_or_5`

When unsure, ask the user which format fits best.

**Body format:**

```
## Problem Details

| Field | Value |
|---|---|
| Platform | {platform} |
| Problem ID | {id or -} |
| Difficulty | {difficulty or -} |
| Link | {link} |

## Problem Statement

{statement or _Not yet captured._}

## Constraints

{constraints or _Not yet captured._}

## Examples

{examples or _Not yet captured._}

## Notes

{notes or _None._}

---

## Solve Checklist

- [ ] `/new-problem` -- scaffold branch and folder
- [ ] Fill in README.md with full problem statement
- [ ] Write solution
- [ ] `/evaluate-solution` -- verify correctness
- [ ] `/solve` -- squash merge and close this issue
```

---

## Step 5 -- Confirm with user

Show the formatted issue title and body.
Ask: "Create this issue in {repo}?"

Do not proceed without confirmation.

---

## Step 6 -- Create the issue

Build the label list:
- Always include: `backlog`, `{platform}`
- Include `{difficulty}` only for leetcode and stratascratch

Run:
```bash
gh issue create \
  --repo {repo} \
  --title "{title}" \
  --body "{body}" \
  --label "backlog" \
  --label "{platform}" \
  [--label "{difficulty}"]
```

Report the created issue URL.
