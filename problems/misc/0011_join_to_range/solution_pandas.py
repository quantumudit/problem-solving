from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent / "data"

# Load source data
customers = pd.read_csv(data_dir / "customer_segment.csv")
regions = pd.read_csv(data_dir / "region_range.csv")

# Pre-parse range strings ("2000-2019") into (low, high) int tuples for fast lookup
region_bounds = [
    (int(lo), int(hi))
    for lo, hi in (r.split("-") for r in regions["Range"].drop_duplicates())
]


def find_range_label(postal_code: int) -> str:
    """Return the range label (e.g. "2000-2019") that contains the given postal code."""
    return next(
        f"{lo}-{hi}" for lo, hi in region_bounds if lo <= postal_code <= hi
    )


# Tag each customer with the range label their postal code falls into
customers["range_label"] = customers["Postal Area"].apply(find_range_label)

# Join to the regions table on the matched range label
matched = customers.merge(regions, how="inner", left_on="range_label", right_on="Range")

# Summarize: count customers per region / sales rep / responder group
summary = (
    matched.groupby(["Region", "Sales Rep", "Responder"])["Customer ID"]
    .count()
    .reset_index()
    .rename(columns={"Customer ID": "Customer Count"})
    .sort_values("Customer Count", ascending=False)
)

show(summary, title="Customers by Region, Sales Rep, and Responder")
