from pathlib import Path

import polars as pl

from utils import show

MONTH_TO_NUMBER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

DATA_FILE = Path(__file__).parent / "data" / "revenues.csv"
revenue_df = pl.read_csv(DATA_FILE).drop_nulls()

revenue_df = revenue_df.with_columns(
    pl.col("Month").replace_strict(MONTH_TO_NUMBER).alias("MonthNo")
).sort("MonthNo")

# Each territory starts as its own owner
unique_territories = revenue_df["Territory"].unique()
ownership = pl.DataFrame({"Territory": unique_territories, "Owner": unique_territories})

months = revenue_df["MonthNo"].unique().sort().to_list()

# Each month: highest-revenue owner acquires all territories of the lowest-revenue owner
for month in months:
    month_df = revenue_df.filter(pl.col("MonthNo") == month).join(
        ownership, on="Territory"
    )

    owner_revenue = month_df.group_by("Owner").agg(pl.sum("Revenue").alias("Revenue"))
    top = owner_revenue.sort("Revenue", descending=True).item(0, "Owner")
    bottom = owner_revenue.sort("Revenue").item(0, "Owner")

    # Only one owner remains -- no more acquisitions possible
    if top == bottom:
        break

    # Reassign every territory owned by bottom to top
    ownership = ownership.with_columns(
        pl.when(pl.col("Owner") == bottom)
        .then(pl.lit(top))
        .otherwise(pl.col("Owner"))
        .alias("Owner")
    )

result = (
    ownership.group_by("Owner")
    .agg(pl.col("Territory").sort().str.join(", ").alias("Territories"))
    .sort("Owner")
)

show(result)
