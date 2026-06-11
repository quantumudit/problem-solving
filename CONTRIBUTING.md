# Contributing

This is a personal problem-solving archive. It is not a collaborative project,
but the setup and workflow are documented here for reference.

---

## Setup

```bash
# Install dependencies
uv sync

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Activate the virtual environment (macOS / Linux)
source .venv/bin/activate
```

---

## Workflow

Each problem lives on its own branch and squash-merges into `main` when solved.
Full conventions are in:

- `docs/conventions.md` -- naming rules, frontmatter fields, branch and commit format
- `docs/structure.md` -- folder layout, file templates, per-platform patterns
- `CLAUDE.md` -- quick reference summary of all conventions

---

## Commit Format

Two commit types are used in this repo:

```
wip: {brief description}
solve: {platform} {id} {slug} [{language}]
```

`wip:` is used freely on problem branches during active work.
`solve:` is the single squash-merge commit that lands on `main`.

Examples:

```
wip: brute force O(n^2)
wip: optimised with hash map
wip: add README and notes
solve: leetcode 0001 two_sum [python]
solve: stratascratch 1234 top_earning_sales [pandas]
solve: excelbi 2025_04_01 sales_by_region [pq]
solve: excelbi 2025_04_01 sales_by_region [pandas, polars]
solve: projects data_with_danny murder_mystery q01 find_the_murderer [sql]
```

No emoji prefixes. No generic tags (`feat`, `fix`, `chore`).
See `docs/conventions.md` for the full rules.
