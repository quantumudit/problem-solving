# Repo Structure

Personal archive of coding problem solutions across multiple platforms. Each problem
lives on its own branch and squash-merges into `main` when solved, building a
cumulative, searchable portfolio over time.

Learnings, tricks, and concept notes live in Obsidian (not here).
Progress analysis lives in a separate project (not here).
This repo's job is to be the clean, structured source of truth for solutions.

---

## Folder Layout

```
problem_solving/
├── CLAUDE.md
├── README.md
├── .gitignore
├── Dockerfile               <- PySpark image (extends apache/spark-py)
├── docker-compose.yml       <- container config (pyspark-lab)
├── .dockerignore
├── justfile                 <- task runner (just excelbi, just excelbi-pyspark, etc.)
├── pyproject.toml           <- Python deps (pandas, polars, duckdb, rich, ...)
├── docs/
│   ├── conventions.md       <- naming rules, commits, frontmatter (source of truth)
│   └── structure.md         <- this file
├── utils/                   <- shared display helpers (display.py)
├── scratchpad/              <- local scratch, rough work, quick experiments (gitignored)
│   └── .gitkeep
├── .claude/
│   ├── settings.json
│   └── skills/              <- Claude Code skills
└── problems/
    ├── leetcode/
    │   ├── easy/
    │   │   └── 0001_two_sum/
    │   ├── medium/
    │   │   └── 0056_merge_intervals/
    │   └── hard/
    │       └── 0023_merge_k_lists/
    ├── stratascratch/
    │   ├── easy/
    │   ├── medium/
    │   │   └── 1234_top_earning_sales/
    │   └── hard/
    ├── excelbi/
    │   └── 2025/
    │       └── 04_01_sales_by_region/
    ├── edna/
    │   └── 2025/
    │       └── w01_customer_churn/
    └── challenges/
        ├── data_with_danny/
        │   └── murder_mystery/
        │       ├── README.md          <- challenge-level readme
        │       ├── data/
        │       ├── q01_find_the_murderer/
        │       └── q02_find_the_witness/
        └── linkedin_learning/
            └── some_course/
```

---

## Platform Structures

| Platform | Has Difficulty | Cadence | Folder Pattern |
|---|---|---|---|
| leetcode | yes | on demand | `problems/leetcode/{difficulty}/{id}_{slug}/` |
| stratascratch | yes | on demand | `problems/stratascratch/{difficulty}/{id}_{slug}/` |
| excelbi | no | daily | `problems/excelbi/{year}/{MM_DD_slug}/` |
| edna | no | weekly | `problems/edna/{year}/{w##_slug}/` |
| challenges | no | challenge set | `problems/challenges/{source}/{challenge}/{q##_slug}/` |

---

## Per-Problem Folder Contents

### Standalone problem (leetcode, stratascratch, excelbi, edna)

```
0001_two_sum/
├── README.md              <- problem statement, link, frontmatter
├── solution.py            <- single solution (or solution_{library}.py for multi-library Python)
└── notes.md               <- approach, complexity, frontmatter
```

For problems solved in multiple Python libraries, name each file after its library:
```
04_01_sales_by_region/
├── README.md
├── data/
│   └── sales.xlsx
├── solution_pandas.py
├── solution_polars.py
└── notes.md
```

### With variations

```
0001_two_sum/
├── README.md
├── solution.py          <- main problem solution
├── solution_v2.py       <- revised attempt at the main problem
├── variations/
│   ├── v1_three_fives.py
│   ├── v2_slug.py
│   └── v3_slug.py
└── notes.md
```

`solution.py` is always the main problem. Variations live in `variations/` prefixed
`v1_`, `v2_`, etc. The branch covers both the main solution and all its variations --
they are one unit of work.

### With a dataset (excelbi, edna, some stratascratch)

```
04_01_sales_by_region/
├── README.md
├── data/
│   └── sales.xlsx
├── solution.pq
└── notes.md
```

### With a mutable dataset (UPDATE / DELETE / INSERT)

```
1234_update_salaries/
├── README.md
├── data/
│   ├── seed.sql        <- committed -- clean starting state
│   └── .gitignore      <- ignores *.db and *.sqlite
├── solution.sql
└── notes.md
```

### Challenge set (challenges/)

Data is shared across all questions -- it lives at the challenge level, not per question.
Individual question folders contain only `solution.*` and `notes.md`.

```
murder_mystery/
├── README.md               <- challenge-level readme with questions index
├── data/
│   └── murder_mystery.db
├── q01_find_the_murderer/
│   ├── solution.sql
│   └── notes.md
└── q02_find_the_witness/
    ├── solution.sql
    └── notes.md
```

---

## File Templates

### README.md -- standalone problems (leetcode, stratascratch, excelbi, edna)

```yaml
---
platform:         # leetcode | stratascratch | excelbi | edna
problem_id:       # quoted string e.g. "0001"
slug:             # snake_case e.g. two_sum
difficulty:       # easy | medium | hard | null
link:             # direct url to the problem
dataset:          # none | provided | mutable | mutable_extracted | mutable_committed
---
```

```markdown
## Problem
[Platform - Problem Title](link)

## Problem Statement
...copy of the problem text...

## Constraints
- ...

## Examples
**Example 1:**
Input: ...
Output: ...

**Example 2:**
Input: ...
Output: ...
```

---

### README.md -- challenge-level only

One README per challenge set, not per question. Acts as the index for all questions.

```yaml
---
platform:         # challenges
source:           # data_with_danny | linkedin_learning | etc.
challenge:        # snake_case challenge name
link:             # url to the challenge or course
dataset:          # filename or description
date_started:     # YYYY-MM-DD
date_completed:   # YYYY-MM-DD | null
---
```

```markdown
## Challenge
[Source - Challenge Title](link)

## Description
...

## Dataset Overview
...tables, schema, what the data represents...

## Questions Index
| # | Slug | Language | Date Solved |
|---|------|----------|-------------|
| q01 | find_the_murderer | sql | 2025-04-01 |
| q02 | find_the_witness  | sql | 2025-04-02 |
```

---

### notes.md -- all problem types

```yaml
---
platform:         # leetcode | stratascratch | excelbi | edna | challenges
problem_id:       # quoted string e.g. "0001" -- omit for challenges
slug:             # snake_case
difficulty:       # easy | medium | hard | null
difficulty_rating: # easy | medium | hard | null -- personal assessment
language:         # always a list e.g. [pandas] or [sql, pandas]; [python] only for pure DSA
topics:           # always a list e.g. [window_functions, cte]
date_solved:      # YYYY-MM-DD
revisit:          # true | false
---
```

```markdown
## Approach
...how you thought about the problem...

## Complexity
- Time:
- Space:

## What tripped me up
...

## Tricks / New Learnings
...specific to this problem...
...anything broader goes to Obsidian with a back-reference to this problem path...

## Variations
- v1_slug -- brief note on what differs
- v2_slug -- brief note on what differs

## Revisit notes
...what to try differently next time...
```

Note: the `## Tricks / New Learnings` heading uses an emoji in the actual file --
this is an established exception to the ASCII-only rule.

---

## Python Solution Code Style

Solution files are standalone -- no shared utilities, no project structure.
Each solution file (`solution.py`, `solution_pandas.py`, etc.) solves one problem
and is read in isolation.

**Structure:**

LeetCode / StrataScatch style (class-based):
```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        ...
```

Pandas / data analysis style (function-based):
```python
import pandas as pd

def top_earning_sales(df: pd.DataFrame) -> pd.DataFrame:
    ...
```

**Key rules:**
- Type hints on all function signatures (parameters and return types)
- Meaningful variable names -- avoid `res`, `ans`, `tmp`, `val`, `data`
- No comments that describe what the code does -- name things well instead
- Add a comment only when the WHY is non-obvious (invariant, edge case, math trick)
- Use built-in generics: `list[int]`, `dict[str, int]` -- not `typing.List`, `typing.Dict`
- Use `X | None` instead of `Optional[X]`
- Line length 88 chars max
- Import only what the solution needs

See the `python-code-style` skill for the full style guide.

---

## Python Virtual Environment

Only needed when a solution imports external packages (pandas, numpy, etc.).
Pure stdlib solutions (most LeetCode algorithm problems) need no setup.

```powershell
# First time setup (repo root)
uv venv

# Add a package
uv add pandas

# Run a solution
uv run python problems/stratascratch/medium/1234_top_earning_sales/solution.py
```

Rules:
- Always `uv add <package>` -- never `pip install` directly
- Always `uv run python <file>` -- never bare `python <file>`
- Never commit `.venv/`, `pyproject.toml`, or `uv.lock`

See the `use-virtual-environment` skill for full setup details.

---

## PySpark / Docker

PySpark solutions (`solution_pyspark.py`) run inside Docker, not via `uv run`.
PySpark is not installed locally -- it lives only in the container.

### Why Docker?

The `apache/spark-py` image ships Spark, Java, and PySpark pre-wired together.
Running PySpark locally would require a separate Java + Spark installation.
Docker keeps it isolated and deletable when not needed.

### Image

`Dockerfile` extends `apache/spark-py:latest` and adds `pandas`, `polars`, and `rich`
(needed by `utils/display.py`). The image is built once and reused.

### Container

`docker-compose.yml` mounts the entire repo into `/workspace` at runtime, so
any file edited locally is immediately visible inside the container.
`PYTHONPATH=/workspace` makes `from utils import show` work.

### Running PySpark solutions

```powershell
# First-time setup (build image + start container)
just spark-create

# Run a solution
just excelbi-pyspark 06_09_case_stage_progress
just excelbi-pyspark 06_09_case_stage_progress v2   # _v2 variant

# Container lifecycle
just spark-up       # start (auto-runs before excelbi-pyspark)
just spark-stop     # stop (keeps container, restartable)
just spark-down     # remove container (image stays cached)
just spark-clean    # remove container + built image
just spark-verify   # check container status + package imports + spark version
```

`just excelbi-pyspark` automatically starts the container if it is not running.

---

## Scratchpad

`scratchpad/` is a local-only workspace for rough work that should never be committed.

Typical uses:
- Quick data exploration and one-off queries
- Jupyter notebooks for problem analysis before writing a clean solution
- Throwaway scripts for testing a library or API
- Any file that is too messy or temporary to belong in a problem folder

Rules:
- Everything inside `scratchpad/` is gitignored via `scratchpad/*`
- Only `.gitkeep` is tracked, to preserve the folder in the repo
- Never move scratchpad content into a problem folder -- rewrite it clean instead

---

## Where Learnings Go

| Type of learning | Where it goes |
|---|---|
| Trick or concept learned from a problem | `notes.md` -- Tricks / New Learnings section |
| Broader concept (e.g. how window functions work) | Obsidian |
| Cross-language comparison (SQL vs pandas) | Obsidian |
| Back-reference from Obsidian to this repo | `-> first seen: stratascratch/medium/1234_top_earning_sales` |

The repo and Obsidian work together:
- Repo = what you solved and how
- Obsidian = what you learned and why it matters

---

## Development Workflow

```
1. /new-problem    -- scaffold branch, folder, README.md skeleton, notes.md, solution file
2. /write-readme   -- fill in README.md from the problem statement
3.  write solution -- solve the problem in solution.py / solution_{library}.py / solution.sql / solution.pq
4. /evaluate-solution -- run examples, generate edge cases, check correctness + complexity
5.  iterate        -- fix issues found by evaluation, re-run /evaluate-solution if needed
6. /solve          -- squash merge with correctly formatted commit message onto main
```

Raw git commands for reference:

```bash
# 1. Start
git checkout main
git checkout -b leetcode/easy/0001_two_sum

# 2. Work -- messy wip commits are fine
git commit -m "wip: brute force"
git commit -m "wip: optimized with hash map"

# 3. Finish -- squash merge
git checkout main
git merge --squash leetcode/easy/0001_two_sum
git commit -m "solve: leetcode 0001 two_sum [python]"
```

---

## .gitignore

```gitignore
# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
pyproject.toml
uv.lock

# Editors
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Mutable databases -- only seed.sql is committed
*.db
*.sqlite

# Guard against large files
*.csv.gz
*.parquet
problems/**/*.zip

# Future R
.Rhistory
.RData
```
