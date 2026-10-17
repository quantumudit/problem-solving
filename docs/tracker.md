# Project Tracker

Active work-in-progress across open branches. Each section is one batch branch.
Update this file as questions are solved and projects close.

---

## Branch: `projects/batch/analytics_scaffold_sep_2026`

Three analytics projects scaffolded and being solved in order: movie ratings, then basketball,
then sales. Merge into `main` once all three are complete.

**Sequence:** movie_ratings_analysis -> basketball_players_analysis -> sales_statistical_analysis

---

### 1. movie_ratings_analysis

**Path:** `projects/misc/movie_ratings_analysis/`
**Stack:** Python, pandas, seaborn, matplotlib
**Status:** IN PROGRESS -- currently active

**Completed:**
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
**Status:** UP NEXT -- scaffold done, no questions solved yet

**Completed:**
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
**Status:** PENDING -- scaffold done, no questions solved yet

**Completed:**
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

### Branch close-out checklist

When all three projects are done:

- [ ] movie_ratings_analysis -- all 7 questions solved
- [ ] basketball_players_analysis -- all 8 questions solved
- [ ] sales_statistical_analysis -- all 13 questions solved
- [ ] All three README.md Insights sections filled
- [ ] All three notes.md filled
- [ ] Push branch: `git push -u origin projects/batch/analytics_scaffold_sep_2026`
- [ ] Squash merge into main
- [ ] Delete branch locally and remotely
