---
name: branching-strategy
description: Branch naming conventions for this problem-solving repo. Apply when creating or naming a branch for a new problem.
---

# Branching Strategy

## Core Rules

- **One branch per unit of work** -- a single standalone problem, or a full challenge set (all questions share one branch)
- **Always branch from `main`**
- **Push to remote immediately** after creating a branch -- every branch must exist on remote from day one
- **Squash merge back to `main`** when the problem is done -- messy WIP commits on the branch are fine and expected
- **Push the branch before merging** -- ensure remote is up to date before running the squash merge
- **Delete local and remote branch after merge** -- once the solve commit is confirmed on main, delete both
- **Never delete a branch that has not been merged** unless the user explicitly asks
- **Never commit solutions directly to `main`**

---

## Branch Naming Format

Branch names are platform-specific. All slugs are snake_case, lowercase.

| Platform | Pattern | Example |
|---|---|---|
| leetcode | `leetcode/{difficulty}/{id}_{slug}` | `leetcode/easy/0001_two_sum` |
| stratascratch | `stratascratch/{difficulty}/{id}_{slug}` | `stratascratch/medium/1234_top_earning_sales` |
| excelbi | `excelbi/{YYYY_MM_DD}_{slug}` | `excelbi/2025_04_01_sales_by_region` |
| edna | `edna/{YYYY_w##}_{slug}` | `edna/2025_w01_customer_churn` |
| challenges | `challenges/{source}/{challenge_name}` | `challenges/data_with_danny/murder_mystery` |

### Rules
- `{difficulty}` is always lowercase: `easy`, `medium`, `hard`
- `{id}` is always zero-padded to 4 digits: `0001`, not `1`
- `{slug}` is always snake_case: `two_sum`, not `twoSum` or `two-sum`
- For challenges, the branch covers the entire challenge set -- not individual questions

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
