---
name: solve
description: Squash-merge the current problem branch into main with the correct commit message, then push and clean up. Use when a problem is finished and ready to be merged.
disable-model-invocation: true
allowed-tools: Bash(git status) Bash(git log *) Bash(git diff *) Bash(git branch *) Bash(git checkout *) Bash(git merge *) Bash(git commit *) Bash(git push *)
---

## Current state

Current branch: !`git branch --show-current`

---

Prepare and run the squash merge for the current problem branch.

### Step 1 -- Parse branch name

Use the branch name injected above to extract commit message components:

| Branch pattern | Extracted fields |
|---|---|
| `leetcode/{difficulty}/{id}_{slug}` | platform, id, slug |
| `stratascratch/{difficulty}/{id}_{slug}` | platform, id, slug |
| `excelbi/{YYYY_MM_DD}_{slug}` | platform, date, slug |
| `edna/{YYYY_w##}_{slug}` | platform, week, slug |
| `challenges/{source}/{challenge}` | platform, source, challenge |

If the branch is `main` or unrecognized, stop and ask the user to switch to a problem branch first.

### Step 2 -- Detect language(s)

Look at solution files in the problem folder:
- `solution.py` or `solution_v*.py` -> `python`
- `solution.sql` -> `sql`
- `solution.pq` -> `pq`
- Multiple solution files -> list all (e.g. `[python, sql]`)

Also check for a `variations/` subfolder -- if present, count the files and note the count.

### Step 3 -- Format commit message

```
solve: {platform} {id} {slug} [{language}]
```

Examples:
```
solve: leetcode 0001 two_sum [python]
solve: stratascratch 1234 top_earning_sales [sql, python]
solve: excelbi 2025_04_01 sales_by_region [pq]
solve: challenges data_with_danny murder_mystery q01 find_the_murderer [sql]
```

If variations exist:
```
solve: leetcode 0001 two_sum + 3 variations [python]
```

### Step 4 -- Confirm with user

Show the proposed commit message and the branch being merged. Confirm before proceeding.
Make clear that this will: push the branch to remote (if needed), squash merge to main,
then delete the branch locally and remotely.

### Step 5 -- Push branch to remote

Before touching main, ensure the branch is fully pushed:

```bash
git push origin {branch_name}
```

If the branch has no upstream yet:
```bash
git push -u origin {branch_name}
```

Do not proceed to the merge if the push fails.

### Step 6 -- Run squash merge

```bash
git checkout main
git merge --squash {branch_name}
git commit -m "solve: ..."
```

Verify the commit landed correctly:
```bash
git log --oneline -3
```

If the commit is not visible on main, stop here. Do not delete the branch.

### Step 7 -- Delete the branch

Only proceed if Step 6 confirmed the solve commit is on main.

```bash
# Delete local branch
# -D is required because squash merge does not record branch history in git
git branch -D {branch_name}

# Delete remote branch
git push origin --delete {branch_name}
```

Confirm both deletions succeeded.

### Step 8 -- Rebuild the index

Run the index script to update `docs/index.md` and `docs/index.csv`:

```bash
python docs/build_index.py
```

The script checks the current branch internally and only rebuilds when on `main`.
If the script fails, report the error but do not roll back the merge -- the index
can be rebuilt at any time by running the script again manually.

Report the final state:
- solve commit on main
- Branch deleted locally and from remote
- Index rebuilt (or note if it failed)
