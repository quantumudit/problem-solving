---
name: raise-pr
description: >
  Full PR lifecycle for this repo -- from branch push to merge to branch cleanup.
  Use this skill whenever the user says "raise a PR", "create a PR", "open a PR",
  "push and PR", "ready to merge", or asks you to handle the PR workflow in any form.
  This covers everything: pushing the branch, writing the PR description, assigning,
  adding to the GitHub project, reporting conflicts, awaiting merge approval,
  post-merge validation, and branch deletion -- all with explicit user gates at
  the right points. Never skip a gate or merge/delete without the user's go-ahead.
---

# raise-pr skill

Full PR lifecycle for this repo. One invocation takes you from a feature branch all
the way to a clean main, with the user approving the two critical gates: merge and
branch deletion.

## Repo context

- **Owner / GitHub username:** `quantumudit`
- **Repo:** `problem-solving`
- **Default base branch:** `main`
- **Solo developer:** no reviewers, no assignees other than the owner
- **GitHub project:** "Data & Coding Challenge Tracker" (the emoji name; search by keyword)

## Required gh scope

Project operations need the `project` scope. If any project command fails with
"missing required scopes", tell the user to run this in a separate terminal and
follow the browser prompt:

```powershell
gh auth refresh -s project
```

Then retry the failed step.

---

## Step 1 -- Push the branch

Check whether the branch is already up to date with remote:

```bash
git status
git push -u origin HEAD
```

If the push fails (diverged history, protected branch, etc.), surface the error and
stop -- do not proceed until the branch is on remote.

---

## Step 2 -- Detect potential conflicts

Compare the branch against main for the files most likely to conflict:

```bash
git diff origin/main...HEAD --name-only
```

Then do a merge-tree check to see if git predicts conflicts:

```bash
git merge-tree $(git merge-base HEAD origin/main) origin/main HEAD
```

Look for conflict markers (`<<<<<<`, `=======`, `>>>>>>`) in the output. If any are
found, note exactly which files and sections are in conflict. You will report this
to the user in Step 5 after the PR is created.

---

## Step 3 -- Write the PR description

This is a solo-developer repo. Keep descriptions short and factual:

- A `## Summary` section with bullet points covering what changed and why
- No test plan, no checklist, no reviewers section
- Match the scope to the branch -- one sentence per logical change is enough

Derive the title from the branch name and the commit messages (`git log --oneline
origin/main..HEAD`).

---

## Step 4 -- Create the PR and assign it

```bash
gh pr create \
  --title "<title>" \
  --body "<description>" \
  --assignee quantumudit \
  --base main
```

Capture the PR URL from the output.

---

## Step 5 -- Report PR status to the user

Tell the user:
- The PR URL
- What was assigned and to whom
- Conflict status:
  - If **no conflicts**: "No merge conflicts detected -- this PR will merge cleanly."
  - If **conflicts exist**: list each conflicted file, describe what sections clash,
    and explain concretely how you plan to resolve each one (which branch's version
    to keep, how to reconcile both sets of changes). Do NOT resolve conflicts yet --
    just present the plan.

---

## Step 6 -- Add to GitHub project and fill fields

### Find the project

```bash
gh project list --owner quantumudit --format json
```

Find the project whose title contains "Data & Coding Challenge Tracker". Note its
`number` and `id`.

### Add the PR to the project

```bash
gh project item-add <number> --owner quantumudit --url <pr-url>
```

Capture the returned item ID.

### List the project's fields

```bash
gh project field-list <number> --owner quantumudit --format json
```

### Fill the fields

For each field, decide the value based on context (branch name, commit messages,
PR description). Fill what you can confidently infer. Common fields and how to fill
them:

| Field | How to fill |
|---|---|
| Status | Set to "In Review" or the closest equivalent option |
| Priority | Infer from the work: bug fixes = high, scaffolding = medium, docs = low |
| Type / Category | Match to the branch prefix: `projects/` -> "Project", `labs/` -> "Lab", `community/` -> "Community", `leetcode/` etc. -> "Problem" |
| Start date | The date of the first commit on the branch |
| End date / Due date | Leave blank unless you can infer it |
| Size / Effort | Infer from number of files changed and commit count |

For single-select fields, list the available options first and pick the best match.

For any field where you are genuinely unsure what value to use -- or where no
available option fits -- do NOT guess silently. Flag it to the user.

### Show the user what was filled

Present a table:

| Field | Value filled | Confident? |
|---|---|---|
| Status | In Review | Yes |
| Priority | Medium | Yes |
| Type | Project | Yes |
| Size | ... | Yes |
| ... | ... | No -- ask |

Ask the user to confirm or correct any "No" rows before moving on.

---

## Step 7 -- Await merge approval (GATE 1)

After showing the project field summary, stop and ask:

> "PR is up at <url>, assigned to you, added to the project. Ready to merge? (yes / no)"

Do NOT proceed to Step 8 until the user says yes. If they say no, wait for further
instructions (they may want to push more commits, edit the description, etc.).

---

## Step 8 -- Merge the PR

When the user approves, merge via the GitHub CLI:

```bash
gh pr merge <pr-url> --squash --delete-branch=false
```

Use `--squash` to keep main's history clean (matches this repo's merge strategy).
Pass `--delete-branch=false` because branch deletion is handled separately in Step 10
after explicit permission.

If the merge fails due to conflicts, resolve them now using the plan described in
Step 5, commit the resolution, push, and retry.

---

## Step 9 -- Switch to main, pull, and validate

```bash
git checkout main
git pull origin main
git log --oneline -5
```

Tell the user:
- The merge commit hash and message
- How many files changed
- That main is now up to date

---

## Step 10 -- Request branch deletion permission (GATE 2)

After reporting the merge status, stop and ask:

> "Merge confirmed on main. OK to delete the branch `<branch-name>` from local and
> remote? (yes / no)"

Do NOT delete anything until the user says yes.

---

## Step 11 -- Delete the branch (local and remote)

When permission is given:

```bash
git branch -D <branch-name>
git push origin --delete <branch-name>
```

Confirm deletion to the user. The workflow is complete.

---

## Edge cases

- **Branch already has an open PR:** `gh pr create` will error. Check first with
  `gh pr list --head <branch>` and surface the existing PR URL instead of creating
  a duplicate.
- **gh project commands unavailable (missing scope):** Tell the user to run
  `gh auth refresh -s project` in a separate terminal, then retry from Step 6.
- **Merge conflict during merge step:** Resolve using the pre-stated plan (Step 5),
  commit, push, then re-trigger the merge.
- **Branch already deleted remotely (e.g., GitHub auto-deleted after merge):**
  Skip the remote delete and only delete locally. Report this to the user.
