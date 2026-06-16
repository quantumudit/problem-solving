---
platform: misc
problem_id: "0009"
slug: sales_chart
difficulty: null
difficulty_rating: easy
language: [matplotlib]
topics: [conditional_logic]
date_solved: 2026-06-14
revisit: false
---

# Notes

## `FormatStrFormatter` -- Custom Axis Tick Labels

By default, matplotlib renders y-axis numbers as plain integers or floats. To
display them in a specific format, pass a `FormatStrFormatter` to the axis formatter.
It uses the same `%`-style format codes as Python's old-style string formatting:

```python
from matplotlib.ticker import FormatStrFormatter

ax.yaxis.set_major_formatter(FormatStrFormatter("$%dK"))
```

`$%dK` breaks down as:
- `$` -- literal dollar sign prefix
- `%d` -- integer format code (drops decimal places)
- `K` -- literal suffix

So a tick value of `35` renders as `$35K`, `48` as `$48K`, and so on. The same
pattern works for the x-axis via `ax.xaxis.set_major_formatter(...)`.

---

## Dynamic Y-Axis Limits with Padding

Hardcoding `ax.set_ylim(20, 50)` breaks the moment the data changes. A better
approach calculates limits from the actual data range and adds proportional padding:

```python
padding = (max(sales) - min(sales)) * 0.10
ax.set_ylim(min(sales) - padding, max(sales) + padding)
```

With `sales = [25, 35, 32, 40, 38, 37, 48, 43, 34, 41, 45, 42]`:
- range = 48 - 25 = 23
- padding = 2.3
- y-limits = (22.7, 50.3)

The 10% factor keeps the line from hugging the top or bottom of the plot regardless
of what data is passed in. Adjusting the multiplier (e.g. 0.15 for more breathing
room) is the only change needed to tune the appearance.

---

## `plt.style.use()` -- Built-in Visual Themes

Matplotlib ships with a set of named style presets that change colors, gridlines,
fonts, and backgrounds in one call:

```python
plt.style.use("seaborn-v0_8-darkgrid")
```

This must be called before creating the figure -- styles apply to everything created
after the call. A few useful built-in styles:

| Style                    | Look                                    |
|--------------------------|-----------------------------------------|
| `seaborn-v0_8-darkgrid`  | Clean dark grid, muted colors           |
| `seaborn-v0_8-whitegrid` | White background with grid lines        |
| `ggplot`                 | R ggplot2 aesthetic, warm palette       |
| `fivethirtyeight`        | Bold colors, minimal borders            |
| `dark_background`        | Full dark canvas, bright lines          |

Run `print(plt.style.available)` to see all styles installed in the current
environment.
