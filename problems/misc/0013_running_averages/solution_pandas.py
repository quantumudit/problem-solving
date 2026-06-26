from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent / "data"

raw_df = pd.read_csv(data_dir / "rm_categories.csv")

# auto-detect ID columns (non-float) vs metric columns (float) without hardcoding names
id_cols = raw_df.select_dtypes(exclude=["float64"]).columns
metric_cols = raw_df.select_dtypes(include=["float64"]).columns

# reshape from wide (one col per metric) to long (one row per metric-observation)
long_df = pd.melt(
    raw_df,
    id_vars=id_cols,
    value_vars=metric_cols,
    var_name="Metric",
    value_name="Value",
)
long_df["Value"] = long_df["Value"].fillna(0)

prepared_df = long_df.sort_values(
    by=["Metric", "RM Category", "Year", "Month"]
).reset_index(drop=True)

# rolling() on a groupby re-adds the group keys as index levels; drop them to align with prepared_df
rolling_3m = (
    prepared_df.groupby(["Metric", "RM Category", "Year"])["Value"]
    .rolling(window=3, min_periods=1)
    .mean()
    .round(2)
    .reset_index(level=[0, 1, 2], drop=True)
    .rename("3M Rolling Avg")
)

rolling_6m = (
    prepared_df.groupby(["Metric", "RM Category", "Year"])["Value"]
    .rolling(window=6, min_periods=1)
    .mean()
    .round(2)
    .reset_index(level=[0, 1, 2], drop=True)
    .rename("6M Rolling Avg")
)

result_df = pd.concat([prepared_df, rolling_3m, rolling_6m], axis=1)

show(result_df, "Rolling Calculations", 10)
