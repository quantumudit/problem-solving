---
name: committing-changes
description: Commit workflow for this problem-solving repo -- covers WIP commits on branches and the full squash merge + cleanup onto main.
---

# Committing Changes

This repo has two distinct commit contexts: working commits on a problem branch,
and the final squash-merge commit onto `main`.

---

## On a problem branch -- WIP commits

Messy commits are expected and fine. Commit as often as useful.

```bash
git add {files}
git status          # confirm what's staged
git commit -m "wip: {brief description}"
```

No format rules enforced on WIP commits. Be descriptive enough to navigate the
branch if you need to revisit.

Examples:
```
wip: brute force O(n^2)
wip: optimized to O(n) with hash map
wip: add README and notes
wip: sql window function approach
```

---

## Finishing a problem -- squash merge onto main

When the solution is complete, follow these steps in order.

### Step 1 -- Review what's on the branch

```bash
git log --oneline main..HEAD    # commits since branching
git diff main                   # full diff vs main
```

Make sure all intended files are present:
- Solution file(s): `solution.py`, `solution_{library}.py`, `solution.sql`, or `solution.pq`
- `README.md` (problem statement and frontmatter filled in)
- `notes.md` (approach, complexity, topics filled in)
- `data/` folder if the problem has a dataset

### Step 2 -- Push branch to remote

Ensure the branch is fully pushed before touching main:

```bash
git push origin {branch_name}
```

Do not proceed to the merge if the push fails.

### Step 3 -- Squash merge

```bash
git checkout main
git merge --squash {branch_name}
git status                      # confirm staged files look right
```

### Step 4 -- Write the solve commit

Follow the `commit-messages` skill for the exact format:

```bash
git commit -m "solve: {platform} {id} {slug} [{language}]"
```

Examples:
```bash
git commit -m "solve: leetcode 0001 two_sum [python]"
git commit -m "solve: stratascratch 1234 top_earning_sales [pandas]"
git commit -m "solve: stratascratch 1234 top_earning_sales [sql, pandas]"
git commit -m "solve: excelbi 2025_04_01 sales_by_region [pq]"
git commit -m "solve: excelbi 2025_04_01 sales_by_region [pandas, polars]"
git commit -m "solve: projects data_with_danny murder_mystery q01 find_the_murderer [sql]"
```

Use the library name (`pandas`, `polars`, `duckdb`, `pyspark`) instead of `python` in the
language bracket whenever an external library is the primary tool. Use `[python]` only for
pure DSA solutions (LeetCode / StrataScatch) that import nothing beyond the standard library.

### Step 5 -- Verify

```bash
git log --oneline -3    # solve commit must be visible on main
```

Do not proceed to deletion if the solve commit is not confirmed here.

### Step 6 -- Delete the branch

Only after the solve commit is confirmed on main:

```bash
# -D is required because squash merge does not record branch history in git
git branch -D {branch_name}
git push origin --delete {branch_name}
```

---

## Pre-merge checklist

```
[ ] All solution files present and complete
[ ] README.md frontmatter filled in (platform, slug, difficulty, link, dataset)
[ ] notes.md frontmatter filled in (topics, language, date_solved)
[ ] No stray test files, scratch files, or editor artifacts staged
[ ] Branch pushed to remote before starting the merge
[ ] solve: commit message follows the correct format
[ ] solve commit verified on main before deleting branch
```

---

## What NOT to do

- Never commit directly to `main` -- always use a branch + squash merge
- Never use `git merge` without `--squash` -- this repo keeps one commit per problem on `main`
- Never run `git add .` blindly -- check `git status` first
- Never merge without pushing the branch to remote first
- Never delete a branch unless the solve commit is confirmed on main
- Never force-delete a branch that has not been merged unless the user explicitly asks
