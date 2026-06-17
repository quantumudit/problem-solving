# Conventions

Single source of truth for all naming rules, frontmatter fields, branch patterns,
commit format, and dataset handling. When in doubt, check here first.

---

## 1. General Naming

Everything snake_case, lowercase, unless stated otherwise.

Exceptions (universal filenames, kept as-is):
- `README.md`
- `notes.md`
- `SKILL.md`
- `CLAUDE.md`

---

## 2. Branch Naming

Every branch represents one unit of work -- a single problem, or a full challenge set.

| Platform | Pattern | Example |
|---|---|---|
| leetcode | `leetcode/{difficulty}/{id}_{slug}` | `leetcode/easy/0001_two_sum` |
| stratascratch | `stratascratch/{difficulty}/{id}_{slug}` | `stratascratch/medium/1234_top_earning_sales` |
| excelbi | `excelbi/{YYYY_MM_DD}_{slug}` | `excelbi/2025_04_01_sales_by_region` |
| edna | `edna/{YYYY_w##}_{slug}` | `edna/2025_w01_customer_churn` |
| misc | `misc/{id}_{slug}` | `misc/0001_two_sum` |
| projects | `projects/{source}/{challenge_name}` | `projects/data_with_danny/murder_mystery` |
| community | `community/{name}/batch_{YYYY_MM}` | `community/microsoft_fabric/batch_2026_06` |

Rules:
- `{difficulty}` always lowercase: `easy`, `medium`, `hard`
- `{id}` always zero-padded to 4 digits: `0001` not `1`
- `{slug}` always snake_case: `two_sum` not `twoSum` or `two-sum`
- For projects, one branch covers the entire project set -- not per question
- For community, one branch covers a batch of contributions (typically a month or quarter)
- Always branch from `main`; never commit solutions directly to `main`
- Push the branch to remote immediately after creation -- every branch must exist on remote from day one
- Push the branch to remote before running the squash merge -- remote must be up to date
- Delete the branch locally and remotely after the solve commit is confirmed on main
- Never delete a branch that has not been merged unless the user explicitly asks

---

## 3. Folder Naming

All folder names: snake_case, lowercase.

### Problem ID padding

```
0001_two_sum       correct
1_two_sum          wrong
```

ExcelBI uses a 2-character series prefix followed by a 5-digit padded number (7 chars total):

| Series | Prefix | Example |
|---|---|---|
| Power Query | `PQ` | `PQ00398` (Power Query Challenge 398) |
| Excel | `EX` | `EX00991` (Excel Challenge 991) |

### Date-based folders (excelbi)

```
04_01_sales_by_region      # MM_DD_slug inside the year folder
```

### Weekly folders (edna)

```
w01_customer_churn         # w##_slug inside the year folder
```

### Course/challenge question folders

```
q01_find_the_murderer      # q##_slug
```

---

## 4. File Naming

| File | Convention |
|---|---|
| Single-language solution | `solution.py` / `solution.sql` / `solution.pq` |
| Multi-library Python solution | `solution_{library}.py` e.g. `solution_pandas.py`, `solution_polars.py` |
| Revised solution (same file) | `solution_v2.py` / `solution_{library}_v2.py` |
| Multi-language same problem | `solution.py` + `solution.sql` (extension differentiates) |
| Variation files | `variations/v1_slug.py`, `variations/v2_slug.py` |
| Seed file | `seed.sql` |
| Dataset | original filename as-is; snake_case if renaming |

**Multi-library Python naming rules:**

- Use `solution_{library}.py` when more than one Python library solves the same problem:
  `solution_pandas.py`, `solution_polars.py`, `solution_duckdb.py`, `solution_pyspark.py`
- Use plain `solution.py` when there is only one Python file (no disambiguation needed),
  or for pure DSA problems (LeetCode / StrataScatch) that use no external library.
- A revised version of a library solution appends `_v2` at the end:
  `solution_pandas_v2.py`, `solution_polars_v2.py`
- `solution_*.py` glob always catches every Python solution file regardless of library.

---

## 5. Difficulty Values

Used in folder structure and frontmatter. Always lowercase:

```
easy | medium | hard | null
```

`null` is used for platforms that do not provide difficulty: excelbi, edna, projects.

`misc` is the catch-all folder for two cases:
- **Unknown source**: problem found somewhere, source lost. Use `platform: misc` in frontmatter.
- **Known but infrequent source**: source is known but does not warrant its own dedicated folder.
  Use the real platform name in frontmatter: `platform: hackerrank`, `platform: projecteuler`, etc.

In both cases the folder is `problems/misc/{id}_{slug}/`. The `platform:` frontmatter field
is the source of truth. The index groups all misc problems under one "Misc" heading with a
Platform column to show the actual source.

For difficulty in `misc`: use the known value if available, otherwise `null`.
The folder structure is always flat -- no difficulty subdirectory regardless of value.

`difficulty_rating` in `notes.md` is a personal assessment. When the platform provides a
difficulty and no override is needed, set it to the same value as `difficulty`. Only use
`null` for platforms without a difficulty (excelbi, edna, projects) or when a personal
rating has not yet been decided.

---

## 6. Dataset Field Values

Used in `README.md` frontmatter:

| Value | Meaning |
|---|---|
| `none` | No dataset needed |
| `platform` | Data lives on the coding platform (StrataScratch, LeetCode, etc.) -- not available locally |
| `provided` | Static file committed as-is |
| `mutable` | Had `seed.sql` from the start |
| `mutable_extracted` | Had `.db`, extracted `seed.sql` from it |
| `mutable_committed` | Had `.db`, committed as-is (extraction not possible) |

---

## 7. Topics Taxonomy

Used in `notes.md` frontmatter. Always snake_case, always a list.

**SQL**
```
window_functions, cte, joins, aggregations, subqueries,
string_manipulation, date_functions, case_when, set_operations,
self_joins, having, update, delete, insert
```

**Python**
```
pandas_groupby, pandas_reshaping, pandas_merge, pandas_filter,
list_comprehensions, datetime, string_ops, lambda_functions
```

**PowerQuery**
```
table_ops, custom_functions, m_language, data_type_handling,
merge_queries, append_queries
```

---

## 8. Language Field Values

Used in `notes.md` frontmatter. Always a list, always lowercase.

For Python, use the library name instead of `python` when an external library is the
primary tool. Use plain `python` only for pure DSA solutions with no external library:

```yaml
language: [sql]
language: [python]          # pure DSA -- no external library (e.g. LeetCode)
language: [pandas]          # pandas solution
language: [polars]          # polars solution
language: [duckdb]          # duckdb solution
language: [pyspark]         # pyspark solution
language: [pandas, polars]  # multiple library solutions for the same problem
language: [python, sql]     # mixed language problem
language: [pq]
```

---

## 9. Commit Format

### `solve:` -- squash merge commits to main (canonical)

```
solve: {platform} {id} {slug} [{language}]
```

| Platform | Example |
|---|---|
| leetcode | `solve: leetcode 0001 two_sum [python]` |
| stratascratch (pandas) | `solve: stratascratch 1234 top_earning_sales [pandas]` |
| stratascratch (sql + pandas) | `solve: stratascratch 1234 top_earning_sales [sql, pandas]` |
| excelbi | `solve: excelbi 2025_04_01 sales_by_region [pq]` |
| excelbi (multi-library) | `solve: excelbi 2025_04_01 sales_by_region [pandas, polars]` |
| edna | `solve: edna 2025_w01 customer_churn [pandas]` |
| misc | `solve: misc 0001 two_sum [python]` |
| projects | `solve: projects data_with_danny murder_mystery q01 find_the_murderer [sql]` |
| community | `solve: community microsoft_fabric 2026_06` |

With variations:
```
solve: leetcode 0001 two_sum + 3 variations [python]
```

Rules:
- `{id}` zero-padded to 4 digits: `0001` not `1`
- `{slug}` snake_case
- `[{language}]` bracketed list, lowercase
- For Python with an external library, use the library name: `[pandas]`, `[polars]`,
  `[duckdb]`, `[pyspark]` -- not `[python]`
- Use `[python]` only for pure DSA solutions with no external library (e.g. LeetCode)
- No period, no emoji, no commit body -- subject line is the entire commit

### `wip:` -- in-progress commits on a branch

```
wip: {brief description}
```

Examples:
```
wip: brute force O(n^2)
wip: optimized with hash map
wip: add notes and README
```

No format rules enforced. Messy `wip:` commits are expected and squashed away before merge.

### What never appears in this repo

- Emoji prefixes (`feat:`, `fix:`, etc.)
- Generic type tags (`feat`, `fix`, `chore`, `refactor`)
- Commit bodies on `solve:` commits

---

## 10. Merge Strategy

Always use `--squash`. One clean commit per problem on `main`.

```bash
# 1. Push branch to remote before merging
git push origin {branch_name}

# 2. Squash merge
git checkout main
git merge --squash {branch_name}
git commit -m "solve: ..."

# 3. Verify the solve commit is on main
git log --oneline -3

# 4. Delete branch locally and remotely
# (-D required: squash merge does not record branch history in git)
git branch -D {branch_name}
git push origin --delete {branch_name}
```

Rules:
- Never use plain `git merge` -- it pollutes `main` with every `wip:` commit
- Never skip the remote push before merging
- Never delete the branch unless the solve commit is confirmed on main
- Never force-delete a branch that was not merged unless the user explicitly asks

---

## 11. Mutable Dataset Workflow

For problems with `UPDATE`, `DELETE`, or `INSERT` solutions:

```bash
# Reset to clean state before every run
sqlite3 data/challenge.db < data/seed.sql

# Run solution
sqlite3 data/challenge.db < solution.sql
```

If the platform provides a `.db` with no `seed.sql`, extract it once:

```bash
sqlite3 data/challenge.db .dump > data/seed.sql
```

Then add to `data/.gitignore`:
```
*.db
*.sqlite
```

Only `seed.sql` is committed. The `.db` file is always regenerated from it.

---

## 12. File Encoding

All scripts, code, config files, and markdown files must use plain ASCII only.
No Unicode characters beyond U+007F.

Common violations to avoid:

| Banned | Replace with |
|---|---|
| em dash (--) | - or -- |
| en dash (-) | - |
| curly quotes (" " ' ') | " or ' |
| ellipsis (...) | ... |
| bullet point (*) | - or * |
| box drawing characters | - or = or \| |

**Exceptions:**
- Content inside fenced code blocks or inline code is exempt
- ASCII art (directory trees, diagrams) is exempt
- The `## Tricks / New Learnings` heading in `notes.md` files uses an emoji
  as part of the defined template -- this specific heading is exempt

See the `script-writing-constraints` skill for the full prohibited character list.
