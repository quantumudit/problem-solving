# problem-solving

Personal archive of coding problem solutions across multiple platforms.
Each problem lives on its own branch and squash-merges into `main` when solved.

> All files in this repo must use plain ASCII only. See `.claude/rules/ascii-only.md`.

**Full docs (source of truth):**
- `docs/conventions.md` -- naming rules, frontmatter fields, branch/commit format, topics, encoding
- `docs/structure.md` -- folder layout, per-platform patterns, file templates, workflow

---

## Repo Layout

```
problem_solving/
├── CLAUDE.md
├── README.md
├── .gitignore
├── Dockerfile              # PySpark image (extends apache/spark-py)
├── docker-compose.yml      # container config for pyspark-lab
├── .dockerignore
├── justfile                # task runner
├── pyproject.toml          # Python deps (pandas, polars, duckdb, rich, ...)
├── docs/
│   ├── conventions.md
│   ├── structure.md
│   ├── index.md        # auto-generated problem index (do not edit manually)
│   └── index.csv       # auto-generated problem index (do not edit manually)
├── utils/              # shared display helpers (display.py)
├── scratchpad/         # local scratch, rough work, quick experiments (gitignored)
├── problems/
│   ├── leetcode/{difficulty}/{id}_{slug}/
│   ├── stratascratch/{difficulty}/{id}_{slug}/
│   ├── excelbi/{year}/{MM_DD_slug}/
│   ├── edna/{year}/{w##_slug}/
│   └── misc/{id}_{slug}/
├── projects/
│   └── {source}/{challenge}/{q##_slug}/
└── community/
    └── {name}/
        ├── README.md              # contribution tracker
        └── solutions/             # code files for non-trivial answers
```

`docs/index.md` and `docs/index.csv` are rebuilt automatically after every `git commit` on `main` via a `PostToolUse` hook. Run `python .claude/hooks/build_index.py` manually to force a rebuild at any time.

---

## Platform Quick Reference

| Platform | Difficulty | ID | Folder pattern |
|---|---|---|---|
| leetcode | easy/medium/hard | 4-digit padded e.g. `"0001"` | `problems/leetcode/{difficulty}/{id}_{slug}/` |
| stratascratch | easy/medium/hard | 4-digit padded e.g. `"1234"` | `problems/stratascratch/{difficulty}/{id}_{slug}/` |
| excelbi | null | `PQ` or `EX` prefix + 5-digit padded e.g. `"PQ00398"`, `"EX00991"` | `problems/excelbi/{year}/{MM_DD_slug}/` |
| edna | null | none | `problems/edna/{year}/{w##_slug}/` |
| misc | null (or known value) | self-assigned, 4-digit padded e.g. `"0001"` | `problems/misc/{id}_{slug}/` |

> `misc` covers two cases: unknown source (`platform: misc`) and known but infrequent source
> (`platform: hackerrank`, `platform: projecteuler`, etc.). Folder is always `problems/misc/`;
> frontmatter `platform:` holds the real source. Index groups all under one "Misc" heading.
| projects | null | none | `projects/{source}/{challenge}/{q##_slug}/` |

---

## Naming Rules

- Everything is **snake_case, lowercase** (except `README.md`, `notes.md`)
- Problem IDs always zero-padded to 4 digits: `0001` not `1`
- Solution files: `solution.py` / `solution.sql` / `solution.pq`
- Multi-library Python: `solution_{library}.py` e.g. `solution_pandas.py`, `solution_polars.py`
- Revised versions: `solution_v2.py`, `solution_{library}_v2.py`
- Variations subfolder: `variations/v1_slug.py`, `variations/v2_slug.py`

---

## Branch Naming

> For full rules and lifecycle, use the `branching-strategy` skill.

```
leetcode/easy/0001_two_sum
stratascratch/medium/1234_top_earning_sales
excelbi/2025_04_01_sales_by_region
edna/2025_w01_customer_churn
misc/0001_two_sum
projects/data_with_danny/murder_mystery
community/microsoft_fabric/batch_2026_06
```

---

## Commit Message Format

> For the full format, WIP commit rules, and examples, see `.claude/rules/commit-messages.md`.

> CRITICAL: Never add a "Co-Authored-By" trailer or any AI attribution to commit messages in this repo.

```
solve: {platform} {id} {slug} [{language}]
```

Examples:
```
solve: leetcode 0001 two_sum [python]
solve: stratascratch 1234 top_earning_sales [pandas]
solve: stratascratch 1234 top_earning_sales [sql, pandas]
solve: excelbi 2025_04_01 sales_by_region [pq]
solve: excelbi 2025_04_01 sales_by_region [pandas, polars]
solve: misc 0001 some_problem [python]
solve: projects data_with_danny murder_mystery q01 find_the_murderer [sql]
solve: community microsoft_fabric 2026_06
```

> For Python solutions: use the library name (`pandas`, `polars`, `duckdb`, `pyspark`)
> instead of `python`. Use `[python]` only for pure DSA with no external library.

---

## Merge Strategy

> For the full pre-merge checklist, use the `committing-changes` skill.
> To run the squash merge interactively, use `/solve`.

Full sequence -- one clean commit per problem on `main`:
```bash
git push origin {branch_name}          # push before merging
git checkout main
git merge --squash {branch_name}
git commit -m "solve: ..."
git branch -D {branch_name}            # -D required after squash merge
git push origin --delete {branch_name}
```

---

## README.md Frontmatter (per problem)

```yaml
---
platform:         # leetcode | stratascratch | excelbi | edna | misc
problem_id:       # quoted string e.g. "0001" -- omit for projects and edna; self-assigned for misc
slug:             # snake_case e.g. two_sum
difficulty:       # easy | medium | hard | null
link:             # direct url to the problem; empty string if source is lost (misc)
dataset:          # none | platform | provided | mutable | mutable_extracted | mutable_committed
---
```

## notes.md Frontmatter (per problem)

```yaml
---
platform:         # leetcode | stratascratch | excelbi | edna | misc | projects
problem_id:       # quoted string e.g. "0001" -- omit for projects and edna; self-assigned for misc
slug:             # snake_case
difficulty:       # easy | medium | hard | null
difficulty_rating: # easy | medium | hard | null -- personal assessment; default to difficulty value when platform provides one
language:         # always a list e.g. [pandas] or [sql, pandas]; [python] only for pure DSA
topics:           # always a list e.g. [window_functions, cte]
date_solved:      # YYYY-MM-DD
revisit:          # true | false
---
```

## Project README Frontmatter (project-level only)

```yaml
---
platform:         # projects
source:           # data_with_danny | linkedin_learning | misc | etc.
challenge:        # snake_case challenge name
link:             # url to the challenge or course
dataset:          # filename or description
date_started:     # YYYY-MM-DD
date_completed:   # YYYY-MM-DD | null
---
```

---

## Topics Taxonomy

**SQL:** `window_functions, cte, joins, aggregations, subqueries, string_manipulation, date_functions, case_when, set_operations, self_joins, having, update, delete, insert`

**Python:** `aggregation, reshaping, joins, filtering, sorting, string_ops, datetime, list_comprehensions, lambda_functions, simulation, stateful_iteration, conditional_logic, recursion, two_pointers, sliding_window, dynamic_programming`

**PowerQuery:** `table_ops, custom_functions, m_language, data_type_handling, merge_queries, append_queries`

---

## Mutable Dataset Workflow

For problems with UPDATE / DELETE / INSERT solutions:
```bash
sqlite3 data/challenge.db < data/seed.sql   # reset to clean state
sqlite3 data/challenge.db < solution.sql    # run solution
```

Only `seed.sql` is committed. Add `*.db` and `*.sqlite` to `data/.gitignore`.

---

## Skills

### User-invoked (`/skill-name`)

| Skill | When to use |
|---|---|
| `/queue-problem` | Found a problem to solve later -- creates a GitHub issue with full details and solve checklist |
| `/new-problem` | Starting a new problem -- scaffolds branch, folder, README.md, notes.md, solution file |
| `/write-readme` | Problem statement is ready -- generates or fills in the per-problem README.md |
| `/evaluate-solution` | Solution is written -- runs examples, generates edge cases, checks correctness and complexity |
| `/solve` | Problem is finished and correct -- runs the squash merge with correctly formatted commit message |

### Always-loaded rules (`.claude/rules/`)

| Rule | Scope |
|---|---|
| `ascii-only` | All files -- plain ASCII characters only |
| `commit-messages` | All commits -- `solve:` and `wip:` format |
| `python-code-style` | Python files only (path-scoped to `**/*.py`) |

### Auto-applied by Claude

| Skill | When Claude applies it |
|---|---|
| `branching-strategy` | Creating or naming a branch |
| `committing-changes` | Staging and committing files |
| `use-virtual-environment` | Running a Python solution that needs external packages |

---

## Running Solutions

Most solutions run via the justfile:

```powershell
just excelbi 06_09_case_stage_progress pandas   # solution_pandas.py via uv run
just excelbi 06_09_case_stage_progress polars   # solution_polars.py via uv run
just excelbi 06_09_case_stage_progress duckdb   # solution_duckdb.py via uv run
```

**PySpark solutions are different -- they run inside Docker, not via `uv run`.**
PySpark is not installed in the local venv; it lives only in the container.

```powershell
just excelbi-pyspark 06_09_case_stage_progress       # solution_pyspark.py
just excelbi-pyspark 06_09_case_stage_progress v2    # solution_pyspark_v2.py
```

`just excelbi-pyspark` auto-starts the container if it is not running.
Use `just spark-create` for first-time setup (build image + start container).
See `docs/structure.md` for full Docker container management commands.
