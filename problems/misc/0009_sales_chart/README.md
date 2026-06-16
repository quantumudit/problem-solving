---
platform: misc
problem_id: "0009"
slug: sales_chart
difficulty: null
link: ""
dataset: none
---

# Sales Chart

A monthly sales line chart built with Matplotlib, exposed through a Typer CLI.
The chart uses a built-in seaborn style, formatted dollar tick labels, and dynamic
y-axis limits that adapt to whatever data is provided.

## Part 1 -- utils.py

### Constants

| Name           | Type             | Description                                    |
|----------------|------------------|------------------------------------------------|
| `MONTHS`       | list[str]        | Month abbreviations Jan-Dec (x-axis labels)    |
| `DEFAULT_SALES`| list[int]        | Default 2023 sales figures in thousands of USD |

Default dataset:

| Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Sales |  25 |  35 |  32 |  40 |  38 |  37 |  48 |  43 |  34 |  41 |  45 |  42 |

### generate_sales_chart(sales)

```python
def generate_sales_chart(sales: list[int | float]) -> None
```

Builds and saves the chart to `sales_trend.png` (200 dpi).

- Style: `seaborn-v0_8-darkgrid`
- Plot: line chart with circular markers at each data point
- X-axis: `MONTHS` labels
- Y-axis: tick labels formatted as `$NK` (e.g. `$35K`, `$50K`) via `FormatStrFormatter`
- Y-limits: dynamic -- 10% padding above and below the data range so the line
  never hugs the edges regardless of the input values
- Closes the figure after saving to release memory

---

## Part 2 -- solution.py

```
python solution.py
python solution.py --sales
python solution.py -s
```

| Flag             | Behaviour                                              |
|------------------|--------------------------------------------------------|
| _(none)_         | Use `DEFAULT_SALES`; print a summary and save chart    |
| `--sales` / `-s` | Prompt for each month's value interactively, then save |

Interactive mode prompts one month at a time and re-prompts on non-numeric input:

```
Enter sales value (in thousands USD) for each month:
  Jan: 28
  Feb: 34
  ...
```

The chart is always saved to `sales_trend.png` in the working directory.
