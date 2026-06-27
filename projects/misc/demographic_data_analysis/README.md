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
  <a href="#questions">Questions</a> •
  <a href="#insights">Insights</a>
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

---

## Insights

The ten questions are designed to progressively peel back the dataset -- starting from
surface-level rankings, moving into distributional patterns, and finally landing on
quantified correlations. Here is what the analysis reveals at each stage.

---

**Ranking and Extremes (q01, q02)**

The top-10 birth rate countries are almost entirely from Sub-Saharan Africa -- Niger
leads at ~49.7 births per 1,000, followed by Angola, Chad, Burundi, and Mali. At the
other end, Hong Kong and Portugal share the lowest birth rate at 7.9, alongside Japan,
Germany, and Greece -- all high-income, ageing-population nations.

For internet usage, the top-10 is dominated by Nordic and Western European countries --
Iceland tops the list at 96.5%, followed by Bermuda, Norway, and Sweden. The bottom-10
is led by Eritrea at just 0.9%, alongside Timor-Leste, Somalia, and Burundi -- countries
that also appear near the top of the birth rate ranking, hinting at a strong inverse
relationship.

---

**Visualizations (q03, q04, q05)**

The scatter plot (q03) makes the inverse relationship unmistakable: countries with high
birth rates cluster in the bottom-left (low internet penetration) while low-birth-rate
countries cluster in the top-right (high internet penetration). The colour-coding by
income group reveals a clean diagonal separation -- each income tier occupies a distinct
band in the chart.

The distribution plots (q04) show that birth rate is right-skewed, with the majority of
countries sitting between 10 and 20 births per 1,000 and a long tail extending toward
50. Internet usage, by contrast, is relatively flat across the 0-100% range with a
slight spike at the low end, indicating many countries still have very limited access.

The box plots (q05) confirm that income group is a strong predictor of both metrics.
High-income countries show tight, low birth rates with high median internet usage. As
income decreases, birth rate medians rise sharply and internet usage medians fall --
with low-income countries showing the widest spread on birth rate, suggesting greater
internal variation within that group.

---

**Income Group Deep Dive (q06, q07, q08, q09, q10)**

The summary table (q06) shows that high-income countries account for the largest group
(67 of 195), with the lowest average birth rate and highest average internet usage.
Low-income countries (30) sit at the opposite extreme on both metrics.

The percentile breakdown (q07) reveals that even within each income group there is
meaningful variation -- particularly in the low-income group, where the interquartile
range for birth rate is wide, meaning not all poor countries have identically high birth
rates.

The extremes analysis (q08) pinpoints which countries pull each income group to its
limits -- useful for spotting outliers that do not fit the group's typical profile.

The above/below global average breakdown (q09) shows that virtually all low-income
countries are above the global average birth rate, while the majority of high-income
countries are below it. The pattern flips cleanly for internet users -- nearly all
high-income countries exceed the global average, while most low-income countries fall
short.

The Pearson correlation (q10) quantifies what the scatter plot suggested: the overall
correlation between birth rate and internet users is strongly negative. When computed
within each income group separately, a negative correlation persists across all four
groups, confirming that the inverse relationship is not just a compositional artifact
of mixing countries from different income levels -- it holds even when controlling for
income group.
