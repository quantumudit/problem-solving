---
name: branching-strategy
description: Branch naming conventions for this problem-solving repo. Apply when creating or naming a branch for a new problem.
---

# Branching Strategy

## Core Rules

- **Two valid branch modes** -- single-problem (one branch per problem) or multi-problem batch (one branch for several problems from the same platform in a session)
- **Always branch from `main`**
- **Push to remote immediately** after creating a branch -- every branch must exist on remote from day one
- **Squash merge back to `main`** when done -- messy WIP commits on the branch are fine and expected
- **Push the branch before merging** -- ensure remote is up to date before running the squash merge
- **Delete local and remote branch after merge** -- once the solve commit is confirmed on main, delete both
- **Never delete a branch that has not been merged** unless the user explicitly asks
- **Never commit solutions directly to `main`**

---

## Branch Naming Format

### Single-Problem Branches

Branch names are platform-specific. All slugs are snake_case, lowercase.

| Platform | Pattern | Example |
|---|---|---|
| leetcode | `leetcode/{difficulty}/{id}_{slug}` | `leetcode/easy/0001_two_sum` |
| stratascratch | `stratascratch/{difficulty}/{id}_{slug}` | `stratascratch/medium/1234_top_earning_sales` |
| excelbi | `excelbi/{YYYY_MM_DD}_{slug}` | `excelbi/2025_04_01_sales_by_region` |
| edna | `edna/{YYYY_w##}_{slug}` | `edna/2025_w01_customer_churn` |
| misc | `misc/{id}_{slug}` | `misc/0001_two_sum` |
| projects | `projects/{source}/{challenge_name}` | `projects/data_with_danny/murder_mystery` |

### Rules
- `{difficulty}` is always lowercase: `easy`, `medium`, `hard`
- `{id}` is always zero-padded to 4 digits: `0001`, not `1`
- `{slug}` is always snake_case: `two_sum`, not `twoSum` or `two-sum`
- For projects, the branch covers the entire project set -- not individual questions

---

### Multi-Problem (Batch) Branches

Use when the user explicitly wants to solve several problems from the same platform in one session.
The branch name encodes the platform and date only -- no problem ID or slug.

| Platform | Pattern | Example |
|---|---|---|
| stratascratch | `stratascratch/batch_{YYYY_MM_DD}` | `stratascratch/batch_2026_06_11` |
| leetcode | `leetcode/batch_{YYYY_MM_DD}` | `leetcode/batch_2026_06_11` |
| excelbi | `excelbi/batch_{YYYY_MM_DD}` | `excelbi/batch_2026_06_11` |

**Merge commit format** -- list every problem solved on the branch:

```
solve: stratascratch batch 2026_06_11 [pandas] -- 1234 slug_one, 5678 slug_two
```

If problems span multiple languages:

```
solve: stratascratch batch 2026_06_11 [sql, pandas] -- 1234 slug_one, 5678 slug_two
```

---

## Branch Lifecycle

```bash
# 1. Create branch and push to remote immediately
git checkout main
git checkout -b leetcode/easy/0001_two_sum
git push -u origin leetcode/easy/0001_two_sum

# 2. Work freely -- wip commits are fine, push as needed
git commit -m "wip: brute force approach"
git commit -m "wip: optimized with hash map"

# 3. Before merging -- ensure remote is up to date
git push origin leetcode/easy/0001_two_sum

# 4. Squash merge
git checkout main
git merge --squash leetcode/easy/0001_two_sum
git commit -m "solve: leetcode 0001 two_sum [python]"

# 5. Verify merge succeeded
git log --oneline -3

# 6. Delete branch locally and remotely
# (-D required because squash merge does not record branch history)
git branch -D leetcode/easy/0001_two_sum
git push origin --delete leetcode/easy/0001_two_sum
```

See the `commit-messages` skill for the exact `solve:` format.
See `/solve` to run steps 3-6 interactively.

---

## What does NOT apply here

- `feat/`, `fix/`, `chore/` prefixes -- those are for software projects, not this repo
- Kebab-case slugs -- this repo uses snake_case throughout
