from pathlib import Path

import polars as pl

from utils import show

data_dir = Path(__file__).parent / "data"
poems = pl.read_csv(data_dir / "poems.csv")

# Define the split expression once (this does not execute yet)
parts = pl.col("Field_1").str.split(",")

cleaned = poems.select(
    parts.list.get(0).str.strip_chars(' "').alias("poem"),
    parts.list.get(1).str.strip_chars().cast(pl.Int64).alias("poem_id"),
    parts.list.get(2)
    .str.strip_chars(" '")
    .str.to_date("%d-%b-%y")
    .alias("poem_read_date"),
)

show(cleaned)
