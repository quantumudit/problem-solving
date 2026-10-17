# Project Tracker

Active and pending work across branches. Each section is one batch branch or standalone task group.
Update this file as tasks are completed and branches are closed.

---

## Branch: `projects/batch/analytics_scaffold_sep_2026` -- MERGED

This branch was squash-merged into `main`. The scaffold and EDA work is done.
All three projects still have unsolved questions -- each will be tackled in its own branch.

**Sequence (original):** movie_ratings_analysis -> basketball_players_analysis -> sales_statistical_analysis

---

### 1. movie_ratings_analysis

**Path:** `projects/misc/movie_ratings_analysis/`
**Stack:** Python, pandas, seaborn, matplotlib
**Branch:** `projects/misc/movie_ratings_analysis` (to be created)
**Status:** PENDING -- scaffold merged, questions not yet started

**Completed (merged):**
- [x] Scaffold project structure (data, scripts, assets, output)
- [x] EDA notebook (`eda.ipynb`) -- fully refactored with insights, key takeaways, filter function

**Questions to solve:**

| # | Question | Script | Done |
|---|----------|--------|------|
| q01 | Top-10 Movies by Budget, RT Ratings, and Audience Ratings | q01_solution_pandas.py | [ ] |
| q02 | Budget Distribution by Genre -- Drama, Drama vs Action, All Genres | q02_solution_pandas.py | [ ] |
| q03 | Critic Ratings Distribution by Genre | q03_solution_pandas.py | [ ] |
| q04 | Correlation -- RT Ratings vs Audience Ratings | q04_solution_pandas.py | [ ] |
| q05 | RT vs Audience Ratings by Genre and Release Year | q05_solution_pandas.py | [ ] |
| q06 | KDE -- RT Ratings vs Audience Ratings | q06_solution_pandas.py | [ ] |
| q07 | KDE -- Budget vs RT Ratings and Budget vs Audience Ratings | q07_solution_pandas.py | [ ] |

**Remaining steps after questions are solved:**
- Fill in `## Insights` section in README.md
- Fill in `notes.md` with observations and pandas patterns learned

---

### 2. basketball_players_analysis

**Path:** `projects/misc/basketball_players_analysis/`
**Stack:** Python, pandas, numpy, matplotlib
**Branch:** `projects/misc/basketball_players_analysis` (to be created)
**Status:** PENDING -- scaffold merged, questions not yet started

**Completed (merged):**
- [x] Scaffold project structure (data, scripts, assets, output)
- [x] YAML source data (`basketball_players.yaml`) + `build_dataset.py`
- [x] EDA notebook skeleton (`eda.ipynb`)

**Pre-requisite:** Run `build_dataset.py` once before starting questions.

```powershell
uv run .\projects\misc\basketball_players_analysis\build_dataset.py
```

**Questions to solve:**

| # | Question | Script | Done |
|---|----------|--------|------|
| q01 | Salary Trend -- All Players | q01_solution_pandas.py | [ ] |
| q02 | Salary per Game and Salary per Field Goal Trend | q02_solution_pandas.py | [ ] |
| q03 | Games Played Trend -- All Players | q03_solution_pandas.py | [ ] |
| q04 | Minutes Played and Points Trend | q04_solution_pandas.py | [ ] |
| q05 | Field Goals per Game and Goal Accuracy Trend | q05_solution_pandas.py | [ ] |
| q06 | Field Goal Attempts per Game and Points per Game Trend | q06_solution_pandas.py | [ ] |
| q07 | Minutes per Game and Field Goals per Minute Trend | q07_solution_pandas.py | [ ] |
| q08 | Points per Field Goal Trend | q08_solution_pandas.py | [ ] |

**Remaining steps after questions are solved:**
- Fill in `## Insights` section in README.md
- Fill in `notes.md` with observations and pandas patterns learned

---

### 3. sales_statistical_analysis

**Path:** `projects/linkedin_learning/sales_statistical_analysis/`
**Stack:** SQL, DuckDB, Python (runner)
**Branch:** `projects/linkedin_learning/sales_statistical_analysis` (to be created)
**Status:** PENDING -- scaffold merged, questions not yet started

**Completed (merged):**
- [x] Scaffold project structure (data, scripts, assets, output)
- [x] pgSQL source data (`storedb.sql`) + `build_dataset.py` (converts to CSV)
- [x] DuckDB runner (`scripts/runner.py`) with typer CLI
- [x] 13 SQL question skeletons across 5 topic groups

**Pre-requisite:** Run `build_dataset.py` once before starting questions.

```powershell
uv run .\projects\linkedin_learning\sales_statistical_analysis\build_dataset.py
```

**Questions to solve:**

| # | Group | Question | Script | Done |
|---|-------|----------|--------|------|
| q01 | Descriptive Statistics | Total number of transactions over the year | q01_solution.sql | [ ] |
| q02 | Descriptive Statistics | Transactions per month | q02_solution.sql | [ ] |
| q03 | Descriptive Statistics | Annual max/min employee shifts | q03_solution.sql | [ ] |
| q04 | Descriptive Statistics | Monthly max/min employee shifts | q04_solution.sql | [ ] |
| q05 | Descriptive Statistics | Total units sold over the year | q05_solution.sql | [ ] |
| q06 | Descriptive Statistics | Total and average units sold per month | q06_solution.sql | [ ] |
| q07 | Descriptive Statistics | Population variance and std dev of units sold per month | q07_solution.sql | [ ] |
| q08 | Percentiles | Discrete percentiles (25th, 50th, 75th, 95th) of daily revenue | q08_solution.sql | [ ] |
| q09 | Percentiles | Continuous percentiles (25th, 50th, 75th, 95th) of daily revenue | q09_solution.sql | [ ] |
| q10 | Correlation | Correlation of units_sold with revenue, employee_shifts, month_of_year | q10_solution.sql | [ ] |
| q11 | Ranking and Mode | Months ranked by total units sold (descending) | q11_solution.sql | [ ] |
| q12 | Ranking and Mode | Most frequent employee shift count per month | q12_solution.sql | [ ] |
| q13 | Linear Regression | Employees needed when units_sold = 1500 (REGR_SLOPE + REGR_INTERCEPT) | q13_solution.sql | [ ] |

**Running a question:**

```powershell
just project-sql linkedin_learning sales_statistical_analysis q01
```

**Remaining steps after questions are solved:**
- Fill in `## Insights` section in README.md
- Fill in `notes.md` with observations and SQL patterns learned

---

## Microsoft Fabric Community -- Backlog Tasks

**Path:** `community/microsoft_fabric/`
**Branch prefix:** `community/microsoft_fabric/...` (one branch per task group)

Three gaps to close, each in its own branch.

---

### Task A: Add missing solution folders (entries 0010-0018)

`contributions.csv` has 18 entries. The `solutions/` folder only covers entries 0001-0009.
Entries 0010-0018 have no solution folder or notes file.

**Branch:** `community/microsoft_fabric/backfill_solutions_0010_0018` (to be created)

| Sno | Title | Has Solution Folder |
|-----|-------|---------------------|
| 0010 | Calculate Distinct Count for Customer excluding names with GOL prefix | [ ] |
| 0011 | Calculating three day weekly and monthly usage and average weekly usage | [ ] |
| 0012 | Cohort analysis - count registrations and first use of service | [ ] |
| 0013 | Percentage at column level by month dividing from a specific subcategory | [ ] |
| 0014 | Return 0% only when the outcome is actually 0 and blank otherwise | [ ] |
| 0015 | Adding Calculated Column with the latest Item (second answer) | [ ] |
| 0016 | Calculating date difference in days within same column | [ ] |
| 0017 | To show Prior Year values for only Current Fiscal Year | [ ] |
| 0018 | Pulling most recent value and excluding blanks | [ ] |

Each folder needs: `notes.md` with the DAX solution and explanation.

---

### Task B: Add .pbix reference files to all solution folders

No solution folder currently has a `.pbix` file. Every entry should have a Power BI
reference file so the DAX can be opened and tested in context.

**Branch:** `community/microsoft_fabric/add_pbix_references` (to be created)

- Add a `.pbix` reference file to each of the 18 solution folders (create folders for
  0010-0018 first -- see Task A)
- The `.pbix` per entry is a minimal file containing the sample data and the DAX measure
  or column from the solution, so the answer can be verified interactively

---

### Task C: Add main tracker .pbix to community root

A single master `.pbix` file at `community/microsoft_fabric/` that tracks all forum
queries as they arrive -- one page or report tab per question answered.

**Branch:** `community/microsoft_fabric/add_main_tracker_pbix` (to be created)

- Source file lives on OneDrive -- copy it into the repo root of this folder
- File name: `microsoft_fabric_community_tracker.pbix` (confirm exact name on copy)
- Add to `.gitignore` if the file is too large to commit; document the OneDrive path in
  `community/microsoft_fabric/README.md` instead

---

## Labs -- Backlog Tasks

**Path:** `labs/` (to be created -- use `/new-lab` skill for each)
**Branch prefix:** `labs/...` (one branch per lab)

Planned labs for hands-on concept exploration through implementation.

| # | Lab Slug | Topic | Status |
|---|----------|-------|--------|
| 01 | rag_fundamentals | Retrieval-Augmented Generation -- chunking, embedding, retrieval, generation | [ ] |
| 02 | langgraph_ltm | LangGraph Long-Term Memory -- stateful agents, memory stores, persistence | [ ] |

Each lab gets its own branch (`labs/{slug}`) and is scaffolded via `/new-lab` before work begins.
Add further lab ideas to this table as they come up.
