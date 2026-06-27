from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "demographic_data.csv")

income_group_summary = (
    df.groupby("Income Group")
    .agg(
        country_count=("Country Name", "count"),
        avg_birth_rate=("Birth Rate", "mean"),
        avg_internet_users=("Internet Users", "mean"),
    )
    .round(2)
    .reset_index()
)

show(income_group_summary, "Demographic Details by Income Group")
