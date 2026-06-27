from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "demographic_data.csv")

cols = ["Income Group", "Country Name"]

# --- Birth Rate extremes per income group ---

min_birth_rate_idx = df.groupby("Income Group")["Birth Rate"].idxmin()
max_birth_rate_idx = df.groupby("Income Group")["Birth Rate"].idxmax()

min_birth_rate = df.loc[min_birth_rate_idx, cols + ["Birth Rate"]].rename(
    columns={"Country Name": "min_country", "Birth Rate": "min_birth_rate"}
)
max_birth_rate = df.loc[max_birth_rate_idx, cols + ["Birth Rate"]].rename(
    columns={"Country Name": "max_country", "Birth Rate": "max_birth_rate"}
)

birth_rate_extremes = min_birth_rate.merge(max_birth_rate, on="Income Group").reset_index(drop=True)

# --- Internet Users extremes per income group ---

min_internet_users_idx = df.groupby("Income Group")["Internet Users"].idxmin()
max_internet_users_idx = df.groupby("Income Group")["Internet Users"].idxmax()

min_internet_users = df.loc[min_internet_users_idx, cols + ["Internet Users"]].rename(
    columns={"Country Name": "min_country", "Internet Users": "min_internet_users"}
)
max_internet_users = df.loc[max_internet_users_idx, cols + ["Internet Users"]].rename(
    columns={"Country Name": "max_country", "Internet Users": "max_internet_users"}
)

internet_users_extremes = min_internet_users.merge(max_internet_users, on="Income Group").reset_index(drop=True)

# --- Output ---

show(birth_rate_extremes, "Birth Rate Min/Max Countries by Income Group")
show(internet_users_extremes, "Internet Users Min/Max Countries by Income Group")
