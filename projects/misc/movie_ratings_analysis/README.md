---
platform: projects
source: misc
challenge: movie_ratings_analysis
link: ""
dataset: provided
date_started: 2026-09-17
date_completed: null
---

![Project Cover](assets/project_cover_image.png)

---

<h4 align="center">
  Analyzing critic and audience ratings of popular movies released
  between 2007-2011 using Python
</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Matplotlib">
  <img src="https://img.shields.io/badge/Seaborn-4c72b0?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Seaborn">
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#dataset">Dataset</a> •
  <a href="#libraries">Libraries</a> •
  <a href="#structure">Structure</a> •
  <a href="#questions">Questions</a> •
  <a href="#insights">Insights</a>
</p>

---

## Overview

This project focuses on analyzing and finding correlations between critic and audience
ratings for popular movies released between 2007 and 2011. The analysis explores rating
distributions, genre-based patterns, budget relationships, and the degree of agreement
between Rotten Tomatoes critic scores and audience scores.

---

## Dataset

**File:** `data/movie_ratings_data.csv` | **Rows:** 560 | **Columns:** 6

| Column | Type | Description |
|--------|------|-------------|
| Film | string | Movie title |
| Genre | string | Movie genre (Action, Adventure, Comedy, Drama, Horror, Thriller) |
| Rotten Tomatoes Ratings % | int | Critic rating from Rotten Tomatoes (0-100) |
| Audience Ratings % | int | Audience rating percentage (0-100) |
| Budget (Mn $) | int | Production budget in millions USD |
| Release Year | int | Year of release (2007-2011) |

---

## Libraries

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading, filtering, aggregation, and groupby analysis |
| `matplotlib` | Base plotting and figure layout |
| `seaborn` | Statistical visualizations (distributions, violin plots, joint plots, KDE) |
| `pathlib` | File path resolution relative to each script (stdlib) |

> Full list: [requirements.txt](requirements.txt)

---

## Structure

```
movie_ratings_analysis/
|-- assets/
|-- data/
|   |-- movie_ratings_data.csv
|-- output/
|-- scripts/
|-- eda.ipynb
|-- notes.md
|-- requirements.txt
|-- README.md
```

<details>
<summary><b>Folder & File Details</b></summary>

<br>

| Name | Description |
|------|-------------|
| `assets/` | Static images used in this README |
| `data/movie_ratings_data.csv` | Source dataset -- 560 movies with ratings, genre, and budget |
| `output/` | Generated chart files saved by visualization scripts (gitignored) |
| `scripts/` | Individual solution scripts, one per question, named `q##_solution_pandas.py` |
| `eda.ipynb` | Exploratory data analysis notebook -- run this first to understand the dataset before diving into the questions |
| `notes.md` | Project notes covering approach, key observations, and pandas tricks learned |
| `requirements.txt` | Python package dependencies |

</details>

---

## Questions

| # | Question | Language | Script |
|---|----------|----------|--------|
| q01 | Top-10 Movies by Budget, RT Ratings, and Audience Ratings | pandas | [q01_solution_pandas.py](scripts/q01_solution_pandas.py) |
| q02 | Budget Distribution by Genre -- Drama, Drama vs Action, All Genres | pandas, seaborn | [q02_solution_pandas.py](scripts/q02_solution_pandas.py) |
| q03 | Critic Ratings Distribution by Genre | pandas, seaborn | [q03_solution_pandas.py](scripts/q03_solution_pandas.py) |
| q04 | Correlation -- RT Ratings vs Audience Ratings | pandas, seaborn | [q04_solution_pandas.py](scripts/q04_solution_pandas.py) |
| q05 | RT vs Audience Ratings by Genre and Release Year | pandas, seaborn | [q05_solution_pandas.py](scripts/q05_solution_pandas.py) |
| q06 | KDE -- RT Ratings vs Audience Ratings | pandas, seaborn | [q06_solution_pandas.py](scripts/q06_solution_pandas.py) |
| q07 | KDE -- Budget vs RT Ratings and Budget vs Audience Ratings | pandas, seaborn | [q07_solution_pandas.py](scripts/q07_solution_pandas.py) |

### Running a Question Script

**From the repo root -- via `just` (recommended):**

```powershell
just project misc movie_ratings_analysis q01
just project misc movie_ratings_analysis q02
# ... same pattern through q07
```

**From the repo root -- via `uv run` directly:**

```powershell
uv run .\projects\misc\movie_ratings_analysis\scripts\q01_solution_pandas.py
```

**From the project folder (`movie_ratings_analysis/`):**

```powershell
uv run scripts\q01_solution_pandas.py
```

---

## Insights

<!-- insights go here -->
