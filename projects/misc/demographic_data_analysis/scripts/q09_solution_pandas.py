from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "demographic_data.csv")

global_avg_birth_rate = df["Birth Rate"].mean()
global_avg_internet_users = df["Internet Users"].mean()

above_below_avg = (
    df.groupby("Income Group")
    .apply(
        lambda g: pd.Series({
            "global_avg_birth_rate": round(global_avg_birth_rate, 2),
            "above_avg_birth_rate": (g["Birth Rate"] > global_avg_birth_rate).sum(),
            "below_avg_birth_rate": (g["Birth Rate"] <= global_avg_birth_rate).sum(),
            "global_avg_internet_users": round(global_avg_internet_users, 2),
            "above_avg_internet_users": (g["Internet Users"] > global_avg_internet_users).sum(),
            "below_avg_internet_users": (g["Internet Users"] <= global_avg_internet_users).sum(),
        }),
        include_groups=False,
    )
    .reset_index()
)

show(above_below_avg, "Above/Below Global Average by Income Group")
