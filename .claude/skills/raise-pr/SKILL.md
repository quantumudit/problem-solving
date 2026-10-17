---
name: raise-pr
description: >
  Full PR lifecycle for this repo -- from branch push to merge to branch cleanup.
  Use this skill whenever the user says "raise a PR", "create a PR", "open a PR",
  "push and PR", "ready to merge", or asks you to handle the PR workflow in any form.
  This covers everything: pushing the branch, writing the PR description, creating
  via GitHub MCP, assigning, adding to the GitHub project, reporting conflicts,
  awaiting merge approval, post-merge validation, and branch deletion -- all with
  explicit user gates at the right points. Never skip a gate or merge/delete without
  the user's go-ahead.
---

# raise-pr skill

Full PR lifecycle for this repo. One invocation takes you from a feature branch all
the way to a clean main, with the user approving the two critical gates: merge and
branch deletion.

## Repo constants

- **owner:** `quantumudit`
- **repo:** `problem-solving`
- **base branch:** `main`
- **merge method:** `squash` (always -- keeps main history clean)
- **assignee:** `quantumudit` (always -- solo developer)
- **GitHub project:** "Data & Coding Challenge Tracker"

## Tool split

| Task | Tool |
|---|---|
| Check for existing PR | `mcp__github__list_pull_requests` |
| Create PR | `mcp__github__create_pull_request` |
| Merge PR | `mcp__github__merge_pull_request` |
| Assign PR | `gh pr edit <number> --assignee quantumudit` |
| Add to project / fill fields | `gh project ...` (needs `project` scope) |
| Push branch, git ops, branch delete | `git` / `gh` CLI |

The GitHub MCP does not support assignees on create/update, and has no project tools,
so those two operations fall back to `gh` CLI.

---

## Step 1 -- Push the branch

```bash
git push -u origin HEAD
```

If the push fails (diverged history, protected branch), surface the error and stop.

---

## Step 2 -- Check for an existing open PR

```
mcp__github__list_pull_requests(
  owner="quantumudit", repo="problem-solving",
  head="quantumudit/<branch-name>", state="open", fields=["number","title","html_url"]
)
```

If one already exists, show the user its URL and stop -- do not create a duplicate.

---

## Step 3 -- Detect potential conflicts

```bash
git merge-tree $(git merge-base HEAD origin/main) origin/main HEAD
```

Scan the output for conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). Note every
conflicted file and section. You will report these in Step 5.

---

## Step 4 -- Write the PR description

Solo-developer repo. Keep descriptions short:
- `## Summary` with bullet points covering what changed and why
- No test plan, no checklist, no reviewer section
- Derive the title from the branch name and `git log --oneline origin/main..HEAD`

---

## Step 5 -- Create the PR via MCP

```
mcp__github__create_pull_request(
  owner="quantumudit",
  repo="problem-solving",
  title="<title>",
  body="<description>",
  head="<branch-name>",
  base="main"
)
```

Capture the PR `number` and `html_url` from the response.

---

## Step 6 -- Assign the PR

The MCP create tool has no assignees field, so use gh CLI:

```bash
gh pr edit <number> --assignee quantumudit
```

---

## Step 7 -- Report PR status to the user

Tell the user:
- PR URL and number
- Assigned to: `quantumudit`
- Conflict status:
  - **No conflicts:** "This PR will merge cleanly."
  - **Conflicts found:** list each file, describe what sections clash, and explain
    your resolution plan concretely (which side to keep, how to reconcile both sets
    of changes). Do NOT resolve yet -- just present the plan and ask for confirmation.

---

## Step 8 -- Add to GitHub project and fill fields

### Find the project number

```bash
gh project list --owner quantumudit --format json
```

Find the entry whose title contains "Data & Coding Challenge Tracker". Note its `number`
and `id`.

### Add the PR to the project

```bash
gh project item-add <number> --owner quantumudit --url <pr-url>
```

Capture the returned item ID.

### List available fields

```bash
gh project field-list <number> --owner quantumudit --format json
```

### Fill the fields

Infer values from the branch name, commit messages, and PR description:

| Field | How to fill |
|---|---|
| Status | "In Review" or closest available option |
| Priority | bug fix -> high, scaffolding/docs -> medium, experiments -> low |
| Type / Category | `projects/` -> "Project", `labs/` -> "Lab", `community/` -> "Community", problem branches -> "Problem" |
| Start date | date of the first commit on the branch |
| End date | leave blank unless clearly inferable |
| Size / Effort | infer from file count and commit count |

For single-select fields, list the available options first and pick the best match.

For any field where you are unsure -- or where no option fits -- flag it rather than
guess silently.

### Show the user what was filled

Present a confirmation table before moving on:

| Field | Value | Confident? |
|---|---|---|
| Status | In Review | Yes |
| Priority | Medium | Yes |
| ... | ... | No -- need your input |

Wait for the user to confirm or correct any "No" rows.

---

## Step 9 -- Await merge approval (GATE 1)

After the project field confirmation, stop and ask:

> "PR #<number> is live at <url>, assigned to you, and added to the project.
> Ready to merge? (yes / no)"

Do NOT proceed to Step 10 until the user explicitly says yes.

---

## Step 10 -- Merge via MCP

```
mcp__github__merge_pull_request(
  owner="quantumudit",
  repo="problem-solving",
  pullNumber=<number>,
  merge_method="squash",
  commit_title="<same as PR title>"
)
```

If the merge is blocked by conflicts, resolve them now using the plan from Step 7,
commit, push, and retry.

---

## Step 11 -- Switch to main, pull, validate

```bash
git checkout main
git pull origin main
git log --oneline -5
```

Report to the user:
- Merge commit hash and title
- Files changed count
- Confirmation that main is up to date

---

## Step 12 -- Request branch deletion permission (GATE 2)

After the merge report, stop and ask:

> "Merge confirmed on main. OK to delete branch `<branch-name>` from local
> and remote? (yes / no)"

Do NOT delete anything until the user says yes.

---

## Step 13 -- Delete the branch

```bash
git branch -D <branch-name>
git push origin --delete <branch-name>
```

Confirm deletion. Workflow complete.

---

## Edge cases

- **Existing open PR:** detected in Step 2 -- show its URL and stop
- **Missing `project` scope:** tell the user to run `gh auth refresh -s project`
  in a separate terminal, then retry from Step 8
- **Merge conflict at merge time:** resolve using the Step 7 plan, commit, push, retry
- **Branch already deleted remotely (GitHub auto-deleted):** skip remote delete,
  only delete locally, and tell the user
