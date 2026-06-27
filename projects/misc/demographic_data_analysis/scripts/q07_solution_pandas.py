from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "demographic_data.csv")

percentile_cols = ["min", "25%", "50%", "75%", "max"]

birth_rate_stats = (
    df.groupby("Income Group")["Birth Rate"]
    .describe()[percentile_cols]
    .round(2)
    .reset_index()
)

internet_users_stats = (
    df.groupby("Income Group")["Internet Users"]
    .describe()[percentile_cols]
    .round(2)
    .reset_index()
)

show(birth_rate_stats, "Birth Rate Distribution Stats by Income Group")
show(internet_users_stats, "Internet Users Distribution Stats by Income Group")
