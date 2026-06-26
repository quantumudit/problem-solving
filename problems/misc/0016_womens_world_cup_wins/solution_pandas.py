from pathlib import Path

import numpy as np
import pandas as pd

from utils import show

data_dir = Path(__file__).parent / "data"

raw_df = pd.read_csv(data_dir / "womens_world_cup.csv", encoding="latin-1")

conditions = [
    raw_df["score_i"] > raw_df["score_j"],
    raw_df["score_i"] < raw_df["score_j"],
]

choices = [
    raw_df["Team_i"],
    raw_df["Team_j"],
]

# draws (equal scores) get default ""; filtered out below via replace + dropna
raw_df["winner"] = np.select(conditions, choices, default="")

wins_df = (
    raw_df["winner"]
    .value_counts()
    .reset_index()
    .replace(r"^\s*$", np.nan, regex=True)
    .dropna(subset=["winner"])
)

wins_df["winner_rank"] = (
    wins_df["count"].rank(ascending=False, method="dense").astype("int64")
)

result_df = wins_df.sort_values("winner_rank").reset_index(drop=True)

show(result_df, "Women's World Cup Wins by Team")

