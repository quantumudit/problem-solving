# Commit Messages

This repo has two commit types -- `wip:` for in-progress work on a branch, and `solve:` for the
final squash-merge commit onto `main`.

---

## `solve:` -- the canonical format

Used only on `main`, as the squash-merge commit that closes a problem branch.

```
solve: {platform} {id} {slug} [{language}]
```

| Platform | Example |
|---|---|
| leetcode | `solve: leetcode 0001 two_sum [python]` |
| stratascratch | `solve: stratascratch 1234 top_earning_sales [pandas]` |
| stratascratch (sql + pandas) | `solve: stratascratch 1234 top_earning_sales [sql, pandas]` |
| excelbi | `solve: excelbi 2025_04_01 sales_by_region [pq]` |
| excelbi (multi-library) | `solve: excelbi 2025_04_01 sales_by_region [pandas, polars]` |
| edna | `solve: edna 2025_w01 customer_churn [pandas]` |
| misc | `solve: misc 0001 two_sum [python]` |
| projects | `solve: projects data_with_danny murder_mystery q01 find_the_murderer [sql]` |

**With variations:**
```
solve: leetcode 0001 two_sum + 3 variations [python]
```

**Multi-library Python:**
```
solve: excelbi 2025_04_01 sales_by_region [pandas, polars]
```

### Rules for `solve:`
- `{id}` always zero-padded to 4 digits: `0001`, not `1`
- `{slug}` always snake_case
- `[{language}]` always a bracketed list, lowercase: `[pandas]`, `[sql]`, `[pq]`, `[sql, pandas]`
- For Python, use the library name: `[pandas]`, `[polars]`, `[duckdb]`, `[pyspark]`
- Use `[python]` only for pure DSA solutions with no external library (e.g. LeetCode)
- Never add a period, emoji, or body -- the subject line is the entire commit

---

## `wip:` -- in-progress commits on a branch

Used freely on problem branches during active work. These are squashed away and never reach `main`.

```
wip: {brief description}
```

Examples:
```
wip: two sum brute force
wip: optimized with hash map
wip: add notes
```

No format rules enforced -- be descriptive enough to navigate the branch history if needed.

---

## What never appears in this repo

- Emoji prefixes -- not used here
- Generic type tags (`feat`, `fix`, `chore`, `refactor`) -- not applicable to problem-solving workflow
- Commit bodies -- `solve:` commits are self-contained; no body needed
