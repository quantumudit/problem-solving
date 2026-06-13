---
platform: misc
problem_id: "0009"
slug: sales_chart
difficulty: null
link: ""
dataset: none
---

# Sales Chart

A parameterized monthly sales visualization built with Matplotlib and
the Cyberpunk visual style. The chart renders a line plot with circular
markers, formatted tick labels, and a gradient fill beneath the line.

## Embedded Dataset (2023)

Monthly sales figures in thousands of USD, used as the default dataset:

| Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Sales |  28 |  32 |  37 |  31 |  40 |  46 |  43 |  51 |  49 |  56 |  62 |  68 |

## Chart Requirements

- Style: Cyberpunk (applied via `mplcyberpunk` or manual dark theme)
- Plot type: line chart with circular markers at each data point
- X-axis: month abbreviations (Jan, Feb, ..., Dec)
- Y-axis: tick labels formatted as "$NK" (e.g., "$35K", "$50K")
  with appropriate axis limits and minor gridlines enabled
- Title: "Monthly Sales Performance -- {year}"
- X-label: "Month"
- Y-label: "Sales (USD)"
- Gradient fill: semi-transparent vertical fill between the plotted line
  and the x-axis to enhance visual depth (use alpha-blended layers or
  a LinearSegmentedColormap fill)

## Function Signature

```python
def plot_sales(
    months: list[str],
    sales: list[float],
    year: int,
    output_path: str | None = None,
) -> None:
    ...
```

- `months`: list of month label strings
- `sales`: corresponding sales values in thousands of USD
- `year`: integer used in the chart title
- `output_path`: if provided, save the figure to this path (PNG);
  if None, display the chart interactively via plt.show()

The function must work with any monthly dataset of matching length, not
just the 2023 data above.

## Entry Point

When the script is run directly, call `plot_sales` with the embedded
2023 dataset:

```
python solution.py
```
