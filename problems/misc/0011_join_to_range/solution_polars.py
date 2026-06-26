from pathlib import Path

import polars as pl

from utils import show

data_dir = Path(__file__).parent / "data"

# Load source data
customers = pl.read_csv(data_dir / "customer_segment.csv")
regions = pl.read_csv(data_dir / "region_range.csv")

# Parse the 'Range' string into numeric bounds natively
regions_parsed = regions.with_columns(
    pl.col("Range").str.split("-").list.first().cast(pl.Int64).alias("low_bound"),
    pl.col("Range").str.split("-").list.last().cast(pl.Int64).alias("high_bound"),
)

# Perform a non-equi join (range match) and aggregate in one pipeline
summary = (
    customers.join_where(
        regions_parsed,
        pl.col("Postal Area") >= pl.col("low_bound"),
        pl.col("Postal Area") <= pl.col("high_bound"),
    )
    .group_by("Region", "Sales Rep", "Responder")
    .agg(pl.len().alias("Customer Count"))
    .sort("Customer Count", descending=True)
)

show(summary, title="Customers by Region, Sales Rep, and Responder")
