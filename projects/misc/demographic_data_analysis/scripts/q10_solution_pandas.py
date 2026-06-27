from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "demographic_data.csv")

overall_corr = round(df["Birth Rate"].corr(df["Internet Users"]), 4)
print(f"Overall Pearson Correlation (Birth Rate vs Internet Users): {overall_corr}")

corr_by_income_group = (
    df.groupby("Income Group")
    .apply(
        lambda g: round(g["Birth Rate"].corr(g["Internet Users"]), 4),
        include_groups=False,
    )
    .reset_index()
    .rename(columns={0: "pearson_correlation"})
)

show(corr_by_income_group, "Pearson Correlation by Income Group")
