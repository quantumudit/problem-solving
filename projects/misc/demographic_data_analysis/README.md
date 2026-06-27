---
platform: projects
source: misc
challenge: demographic_data_analysis
link: ""
dataset: provided
date_started: 2026-06-27
date_completed: null
---

![Project Cover](assets/project_cover_image.png)

---

<h4 align="center">
  Analyzing demographic details using various metrics across 195 countries
  using Python
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
  <a href="#questions">Questions</a>
</p>

---

## Overview

This mini project explores and finds correlations between three demographic metrics -- birth rate, internet users, and income group -- across 195 countries. The analysis is structured as a series of focused questions, progressing from simple filtering and ranking to distribution analysis, income group comparisons, and correlation studies.

---

## Dataset

**File:** `data/demographic_data.csv` | **Rows:** 195 | **Columns:** 5

| Column | Type | Description |
|--------|------|-------------|
| Country Name | string | Full name of the country |
| Country Code | string | ISO 3-letter country code (e.g. IND, USA) |
| Birth Rate | float | Number of live births per 1,000 population |
| Internet Users | float | Percentage of the population using the internet |
| Income Group | string | World Bank income classification |

**Income Group values:** `High income`, `Upper middle income`, `Lower middle income`, `Low income`

---

## Libraries

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading, filtering, aggregation, and groupby analysis |
| `matplotlib` | Base plotting and figure layout |
| `seaborn` | Statistical visualizations (histograms, box plots, scatter plots) |
| `pathlib` | File path resolution relative to each script (stdlib) |

> Full list: [requirements.txt](requirements.txt)

---

## Structure

```
demographic_data_analysis/
|-- assets/
|-- data/
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
| `data/` | Source dataset (`demographic_data.csv`) |
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
| q01 | Top and Bottom 10 Countries by Birth Rate | pandas | [q01_solution_pandas.py](scripts/q01_solution_pandas.py) |
| q02 | Top and Bottom 10 Countries by Internet Users | pandas | [q02_solution_pandas.py](scripts/q02_solution_pandas.py) |
| q03 | Correlation between Birth Rate and Internet Users - Scatterplot | pandas, seaborn | [q03_solution_pandas.py](scripts/q03_solution_pandas.py) |
| q04 | Birth Rate and Internet Users Distribution - Histogram & KDE | pandas, seaborn | [q04_solution_pandas.py](scripts/q04_solution_pandas.py) |
| q05 | Birth Rate and Internet Users by Income Group - Box Plots | pandas, seaborn | [q05_solution_pandas.py](scripts/q05_solution_pandas.py) |
| q06 | Demographic Details by Income Group | pandas | [q06_solution_pandas.py](scripts/q06_solution_pandas.py) |
| q07 | Distribution Stats by Income Group | pandas | [q07_solution_pandas.py](scripts/q07_solution_pandas.py) |
| q08 | Min/Max Countries by Birth Rate and Internet Users | pandas | [q08_solution_pandas.py](scripts/q08_solution_pandas.py) |
| q09 | Above/Below Global Average by Income Group | pandas | [q09_solution_pandas.py](scripts/q09_solution_pandas.py) |
| q10 | Pearson Correlation Overall and by Income Group | pandas | [q10_solution_pandas.py](scripts/q10_solution_pandas.py) |
