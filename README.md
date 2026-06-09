# problem-solving

Personal archive of coding problem solutions across multiple platforms.
Each problem lives on its own branch and squash-merges into `main` when solved.

## Platforms

| Platform | Folder |
|---|---|
| LeetCode | `problems/leetcode/{difficulty}/{id}_{slug}/` |
| StrataScratch | `problems/stratascratch/{difficulty}/{id}_{slug}/` |
| ExcelBI | `problems/excelbi/{year}/{MM_DD_slug}/` |
| EDNA | `problems/edna/{year}/{w##_slug}/` |
| Challenges | `problems/challenges/{source}/{challenge}/{q##_slug}/` |

## Running Solutions

Most solutions run via `uv run` through the justfile:

```powershell
just excelbi 06_09_case_stage_progress pandas    # solution_pandas.py
just excelbi 06_09_case_stage_progress polars    # solution_polars.py
just excelbi 06_09_case_stage_progress duckdb    # solution_duckdb.py
```

PySpark solutions run inside Docker (see `Dockerfile` and `docker-compose.yml`):

```powershell
just excelbi-pyspark 06_09_case_stage_progress   # solution_pyspark.py
just excelbi-pyspark 06_09_case_stage_progress v2  # solution_pyspark_v2.py
```

Docker container management:

```powershell
just spark-create    # build image + start container (first-time setup)
just spark-up        # start container
just spark-stop      # stop container
just spark-down      # remove container (image kept)
just spark-clean     # remove container + image
just spark-verify    # confirm setup is healthy
```

## Index

See `docs/index.md` for the full problem index (auto-generated).
